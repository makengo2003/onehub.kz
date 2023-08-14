from typing import Mapping, Tuple, TypeVar, Optional
from datetime import datetime
from typing_extensions import TypeAlias

from admin_actions.models import AdminAction
from project.utils import datetime_now
from dateutil.relativedelta import relativedelta

from project import settings
from django.db.models import Q

from resident.models import Resident
from booking.forms import AddBookedPlaceForm, RenewBookedPlaceForm
from booking.models import BookingRequest, BookedPlace, AcceptedBookingRequest

T = TypeVar("T")
Success: TypeAlias = bool
StatusCode: TypeAlias = int
Message: TypeAlias = str


def calculate_booking_expires_at_dt(booking_starts_at: datetime, duration: int, term: str,
                                    time_type: str) -> datetime:
    if term.startswith("hours"):
        return booking_starts_at + relativedelta(hours=duration)
    else:
        if term.startswith("days"):
            booking_expires_at = booking_starts_at + relativedelta(days=duration)
        elif term.startswith("weeks"):
            booking_expires_at = booking_starts_at + relativedelta(weeks=duration)
        else:  # term.startswith("months")
            booking_expires_at = booking_starts_at + relativedelta(months=duration)

        days = 1  # if time_type == "daytime"
        hour = 22
        if time_type == "nighttime":
            days = (booking_expires_at.time().hour < 8)
            hour = 8

        booking_expires_at = booking_expires_at - relativedelta(days=days)
        booking_expires_at = booking_expires_at.replace(hour=hour, minute=0)

        return booking_expires_at


def place_is_free_at_given_dt(place_number: str, time_type: str, booking_starts_at: datetime,
                              booking_expires_at: datetime, booked_place_id: Optional[int] = 0,
                              resident_id: Optional[int] = 0) -> bool:
    booked_places = BookedPlace.objects.filter(Q(time_type=time_type) | Q(time_type="day"), status="active",
                                               number=place_number).only("starts_at", "expires_at")

    for booked_place in booked_places:
        if booked_place.id != booked_place_id:
            condition1 = booking_expires_at.replace(second=0,
                                                    microsecond=0).timestamp() <= booked_place.starts_at.replace(
                second=0,
                microsecond=0
            ).timestamp()
            condition2 = booking_starts_at.replace(second=0,
                                                   microsecond=0).timestamp() >= booked_place.expires_at.replace(
                second=0,
                microsecond=0
            ).timestamp()
            if not (condition1 or condition2):
                return False

    residents = Resident.objects.filter(Q(time_type=time_type) | Q(time_type="day"), status="active",
                                        place_number=place_number).only("starts_at", "expires_at")

    for resident in residents:
        if resident.id != resident_id:
            condition1 = booking_expires_at.replace(second=0, microsecond=0) <= resident.starts_at.replace(
                second=0,
                microsecond=0
            )
            condition2 = booking_starts_at.replace(second=0, microsecond=0) >= resident.expires_at.replace(
                second=0,
                microsecond=0
            )
            if not (condition1 or condition2):
                return False

    return True


def _make_booking_request_accepted(booking_request_id: int, booked_place_id: int) -> None:
    BookingRequest.objects.filter(id=booking_request_id).update(is_accepted=True, answered_at=datetime_now())
    AcceptedBookingRequest.objects.create(booking_request_id=booking_request_id, booked_place_id=booked_place_id)


def add_booked_place(booked_place_info: Mapping) -> Tuple[Success, StatusCode, Message]:
    form = AddBookedPlaceForm(booked_place_info)

    if form.is_valid():
        booking_starts_at = form.cleaned_data.get("starts_at")
        booking_expires_at = calculate_booking_expires_at_dt(
            booking_starts_at,
            form.cleaned_data["duration"],
            form.cleaned_data["term"],
            form.cleaned_data["time_type"]
        )

        if form.cleaned_data["number"]:
            if not place_is_free_at_given_dt(form.cleaned_data["number"], form.cleaned_data["time_type"],
                                             booking_starts_at, booking_expires_at):
                return False, 409, "Place is not free at given datetime"

        booked_place = form.save(commit=False)
        booked_place.expires_at = booking_expires_at
        booked_place.save()

        request_user = getattr(settings, 'request_user', None)

        if form.cleaned_data["booking_request_id"] > 0:
            _make_booking_request_accepted(form.cleaned_data["booking_request_id"], booked_place.id)
            title = f"Принял(а) запрос и забронировал {booked_place.type} для {booked_place.consumer_fullname}" \
                    f"({booked_place.starts_at.strftime('%d.%m.%Y, %H:%M')} --- {booked_place.expires_at.strftime('%d.%m.%Y, %H:%M')})"
        else:
            title = f"Забронировал(а) {booked_place.type} для {booked_place.consumer_fullname}" \
                    f"({booked_place.starts_at.strftime('%d.%m.%Y, %H:%M')} --- {booked_place.expires_at.strftime('%d.%m.%Y, %H:%M')})"

        AdminAction.objects.create(admin_fullname=request_user.username,
                                   title=title)
        return True, 201, "Created"
    return False, 400, str(dict(form.errors))


def renew_booked_place(booked_place_info: Mapping) -> Tuple[Success, StatusCode, Message]:
    form = RenewBookedPlaceForm(booked_place_info)
    if form.is_valid():
        booked_place = BookedPlace.objects.filter(id=form.cleaned_data["booked_place_id"])[0]
        booking_expires_at = calculate_booking_expires_at_dt(
            booked_place.expires_at,
            form.cleaned_data["duration"],
            form.cleaned_data["term"],
            form.cleaned_data["time_type"]
        )

        if booked_place.number:
            if not place_is_free_at_given_dt(booked_place.number, form.cleaned_data["time_type"],
                                             booked_place.expires_at, booking_expires_at,
                                             booked_place_id=form.cleaned_data["booked_place_id"]):
                return False, 409, "Place is not free at given datetime"

        booked_place.status = "deleted"
        booked_place.deleted_at = datetime_now()
        booked_place.save(update_fields=["status", "deleted_at"])

        booked_place_dict = booked_place.__dict__
        del booked_place_dict["_state"], booked_place_dict["id"]

        new_booked_place = BookedPlace(**booked_place.__dict__)
        new_booked_place.id = None

        new_booked_place.status = "active"
        new_booked_place.deleted_at = None
        new_booked_place.starts_at = booked_place.expires_at
        new_booked_place.expires_at = booking_expires_at
        new_booked_place.duration = form.cleaned_data["duration"]
        new_booked_place.term = form.cleaned_data["term"]
        new_booked_place.time_type = form.cleaned_data["time_type"]
        new_booked_place.save()

        request_user = getattr(settings, 'request_user', None)
        AdminAction.objects.create(admin_fullname=request_user.username,
                                   title=f"Продлил(а) забронированного место для {new_booked_place.consumer_fullname} "
                                         f"({new_booked_place.starts_at.strftime('%d.%m.%Y, %H:%M')} --- {new_booked_place.expires_at.strftime('%d.%m.%Y, %H:%M')})")

        return True, 200, "OK"
    return False, 400, "Bad Request"


def delete_booked_place(booked_place_id: int) -> None:
    booked_place = BookedPlace.objects.filter(id=booked_place_id).only("consumer_fullname",
                                                                       "starts_at", "expires_at").first()
    booked_place.status = "deleted"
    booked_place.deleted_at = datetime_now()
    booked_place.save(update_fields=["status", "deleted_at"])

    request_user = getattr(settings, 'request_user', None)
    AdminAction.objects.create(admin_fullname=request_user.username,
                               title=f"Удалил(а) забронированного место {booked_place.consumer_fullname} "
                                     f"({booked_place.starts_at.strftime('%d.%m.%Y, %H:%M')} --- {booked_place.expires_at.strftime('%d.%m.%Y, %H:%M')})")


def update_booked_place_info(booked_place_id: int, field_for_updating: str, new_value: T) -> None:
    BookedPlace.objects.filter(id=booked_place_id).update(**{field_for_updating: new_value})


def search_by_fullname(fullname):
    booked_place = BookedPlace.objects.filter(consumer_fullname__icontains=fullname).only("consumer_phone_number").first()
    if booked_place:
        return str(booked_place.consumer_phone_number)
    return ""


def search_by_phone_number(phone_number):
    booked_place = BookedPlace.objects.filter(consumer_phone_number__icontains=phone_number.replace(" ", "+")).only("consumer_fullname").first()
    if booked_place:
        return booked_place.consumer_fullname
    return ""
