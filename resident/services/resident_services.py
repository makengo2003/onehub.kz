from typing import Mapping, Tuple

from dateutil.relativedelta import relativedelta
from project import settings
from django.db.models import Q

from admin_actions.models import AdminAction
from booking.services import booked_place_services as booking_services
from booking.models import FromBookedPlaceToResident, BookedPlace
from booking.services.booked_place_services import Message, StatusCode, Success, T

from project.utils import datetime_now
from site_settings.models import PlaceTypePrice

from resident.forms import AddResidentForm, RenewResidentForm
from resident.models import Resident, ResidentVisitedDay


def _calculate_price(place_type: str, time_type: str, duration: int, term: str, discount: int) -> int:
    place_type_price = PlaceTypePrice.objects.filter(Q(time_type=time_type) | Q(time_type="anytime"),
                                                     place_type__name=place_type, duration=duration,
                                                     term=term).only("price")
    if not place_type_price:
        place_type_price = PlaceTypePrice.objects.filter(Q(time_type=time_type) | Q(time_type="anytime"),
                                                         place_type__name=place_type, duration=1,
                                                         term=term).only("price")[0]
        price = duration * place_type_price.price
    else:
        price = place_type_price[0].price

    return price - (price * (discount / 100.0))


def calculate_resident_adding_price(resident_info: Mapping) -> Tuple[Success, StatusCode, Message, int]:
    form = AddResidentForm(resident_info)
    if form.is_valid():
        booking_starts_at = form.cleaned_data.get("starts_at")
        booking_expires_at = booking_services.calculate_booking_expires_at_dt(
            booking_starts_at,
            form.cleaned_data["duration"],
            form.cleaned_data["term"],
            form.cleaned_data["time_type"]
        )

        if form.cleaned_data["place_number"]:
            if not booking_services.place_is_free_at_given_dt(form.cleaned_data["place_number"],
                                                              form.cleaned_data["time_type"],
                                                              booking_starts_at, booking_expires_at,
                                                              booked_place_id=form.cleaned_data["booked_place_id"]):
                return False, 409, "Place is not free at given datetime", 0

        return True, 200, "OK", _calculate_price(form.cleaned_data.get("place_type"),
                                                 form.cleaned_data.get("time_type"),
                                                 form.cleaned_data.get("duration"),
                                                 form.cleaned_data.get("term"),
                                                 form.cleaned_data.get("used_discount"))
    return False, 400, str(dict(form.errors)), 0


def calculate_resident_renewing_price(resident_info: Mapping) -> Tuple[Success, StatusCode, Message, int]:
    form = RenewResidentForm(resident_info)

    if form.is_valid():
        resident = Resident.objects.filter(id=form.cleaned_data["resident_id"]).only("id", "place_number",
                                                                                     "expires_at")[0]
        booking_expires_at = booking_services.calculate_booking_expires_at_dt(
            resident.expires_at,
            form.cleaned_data["duration"],
            form.cleaned_data["term"],
            form.cleaned_data["time_type"]
        )

        if resident.place_number:
            if not booking_services.place_is_free_at_given_dt(resident.place_number, form.cleaned_data["time_type"],
                                                              resident.expires_at, booking_expires_at,
                                                              resident_id=resident.id):
                return False, 409, "Place is not free at given datetime", 0

        return True, 200, "OK", _calculate_price(resident.place_type,
                                                 form.cleaned_data["time_type"],
                                                 form.cleaned_data["duration"],
                                                 form.cleaned_data["term"],
                                                 form.cleaned_data["used_discount"])
    return False, 400, "Bad Request", 0


def _make_from_booked_place_to_resident(booked_place_id: int, resident: Resident) -> None:
    booked_place = BookedPlace.objects.filter(id=booked_place_id)[0]
    resident.created_at = booked_place.starts_at

    if not resident.pk:
        resident.save()
    else:
        resident.save(update_fields=["created_at"])

    booked_place.status = "deleted"
    booked_place.deleted_at = datetime_now()
    booked_place.save(update_fields=["status", "deleted_at"])
    FromBookedPlaceToResident.objects.create(booked_place_id=booked_place_id,
                                             resident_id=resident.pk)


def add_resident(resident_info: Mapping) -> Tuple[Success, StatusCode, Message]:
    form = AddResidentForm(resident_info)

    if form.is_valid():
        booking_starts_at = form.cleaned_data.get("starts_at")
        booking_expires_at = booking_services.calculate_booking_expires_at_dt(
            booking_starts_at,
            form.cleaned_data["duration"],
            form.cleaned_data["term"],
            form.cleaned_data["time_type"]
        )

        if form.cleaned_data["place_number"]:
            if not booking_services.place_is_free_at_given_dt(form.cleaned_data["place_number"],
                                                              form.cleaned_data["time_type"],
                                                              booking_starts_at, booking_expires_at,
                                                              booked_place_id=form.cleaned_data["booked_place_id"]):
                return False, 409, "Place is not free at given datetime"

        resident = form.save(commit=False)
        resident.expires_at = booking_expires_at
        resident.price = _calculate_price(form.cleaned_data["place_type"],
                                          form.cleaned_data["time_type"],
                                          form.cleaned_data["duration"],
                                          form.cleaned_data["term"],
                                          form.cleaned_data["used_discount"])
        resident.save()

        request_user = getattr(settings, 'request_user', None)

        if form.cleaned_data["booked_place_id"] > 0:
            _make_from_booked_place_to_resident(form.cleaned_data["booked_place_id"], resident)
            title = f"Сделал(а) резидентом {resident.fullname} ({resident.starts_at.strftime('%d.%m.%Y, %H:%M')} --- {resident.expires_at.strftime('%d.%m.%Y, %H:%M')}) после бронирования места"
        else:
            title = f"Добавил(а) резидента {resident.fullname} ({resident.starts_at.strftime('%d.%m.%Y, %H:%M')} --- {resident.expires_at.strftime('%d.%m.%Y, %H:%M')})"

        AdminAction.objects.create(admin_fullname=request_user.username,
                                   title=title)
        return True, 201, "Created"
    return False, 400, "Bad Request"


def renew_resident(resident_info: Mapping) -> Tuple[Success, StatusCode, Message]:
    form = RenewResidentForm(resident_info)

    if form.is_valid():
        resident = Resident.objects.filter(id=form.cleaned_data["resident_id"])[0]
        booking_expires_at = booking_services.calculate_booking_expires_at_dt(
            resident.expires_at,
            form.cleaned_data["duration"],
            form.cleaned_data["term"],
            form.cleaned_data["time_type"]
        )

        if resident.place_number:
            if not booking_services.place_is_free_at_given_dt(resident.place_number, form.cleaned_data["time_type"],
                                                              resident.expires_at, booking_expires_at,
                                                              resident_id=resident.id):
                return False, 409, "Place is not free at given datetime"

        resident.status = "deleted"
        resident.deleted_at = datetime_now()
        resident.save(update_fields=["status", "deleted_at"])

        resident_dict = resident.__dict__
        del resident_dict["_state"], resident_dict["id"]

        new_resident = Resident(**resident.__dict__)
        new_resident.id = None

        new_resident.status = "active"
        new_resident.deleted_at = None
        new_resident.starts_at = resident.expires_at
        new_resident.expires_at = booking_expires_at
        new_resident.duration = form.cleaned_data["duration"]
        new_resident.term = form.cleaned_data["term"]
        new_resident.time_type = form.cleaned_data["time_type"]
        new_resident.used_discount = form.cleaned_data["used_discount"]
        new_resident.payment_type = form.cleaned_data["payment_type"]
        new_resident.price = _calculate_price(resident.place_type, form.cleaned_data["time_type"],
                                              form.cleaned_data["duration"], form.cleaned_data["term"],
                                              form.cleaned_data["used_discount"])
        new_resident.save()

        request_user = getattr(settings, 'request_user', None)
        AdminAction.objects.create(admin_fullname=request_user.username,
                                   title=f"Сделал(а) продление для резидента {new_resident.fullname} "
                                         f"({new_resident.starts_at.strftime('%d.%m.%Y, %H:%M')} --- {new_resident.expires_at.strftime('%d.%m.%Y, %H:%M')})")
        return True, 200, "OK"
    return False, 400, "Bad Request"


def delete_resident(resident_id: int) -> None:
    resident = Resident.objects.filter(id=resident_id).only("fullname", "starts_at", "expires_at").first()
    resident.status = "deleted"
    resident.deleted_at = datetime_now()
    resident.save(update_fields=["status", "deleted_at"])
    request_user = getattr(settings, 'request_user', None)
    AdminAction.objects.create(admin_fullname=request_user.username,
                               title=f"Удалил(а) резидента {resident.fullname} "
                                     f"({resident.starts_at.strftime('%d.%m.%Y, %H:%M')} --- {resident.expires_at.strftime('%d.%m.%Y, %H:%M')})")


def update_resident_info(resident_id: int, field_for_updating: str, new_value: T) -> None:
    Resident.objects.filter(id=resident_id).update(**{field_for_updating: new_value})


def update_resident_visited_today_status(resident_id: int) -> None:
    resident_visited_day, created = ResidentVisitedDay.objects.get_or_create(resident_id=resident_id,
                                                                             date=datetime_now().date())
    if not created:
        resident_visited_day.delete()


def get_attendance_of_resident(resident_id: int) -> Mapping:
    resident = Resident.objects.filter(id=resident_id).only("starts_at", "expires_at")[0]
    starts_at_date = resident.starts_at.date()
    expires_at_date = resident.expires_at.date()

    today = datetime_now().date()
    attendance_of_resident = dict()
    max_possible_visited_days_count = (expires_at_date - starts_at_date).days

    for i in range(max_possible_visited_days_count):
        date = (starts_at_date + relativedelta(days=i + 1)).date()
        if date < today:
            attendance_of_resident[str(date)] = False
        else:
            attendance_of_resident[str(date)] = None

    visited_dates = resident.visited_days.all().only("date")

    for i, visited_date in enumerate(visited_dates):
        attendance_of_resident[str(visited_date)] = True

        if visited_dates[i - 1] == visited_date:
            attendance_of_resident[str((visited_date - relativedelta(days=1)).date())] = True

    return attendance_of_resident


def search_by_fullname(fullname):
    resident = Resident.objects.filter(fullname__icontains=fullname).only("phone_number", "profession").first()
    if resident:
        return str(resident.phone_number), resident.profession
    return "", ""


def search_by_phone_number(phone_number):
    resident = Resident.objects.filter(phone_number__icontains=phone_number.replace(" ", "+")).only("fullname", "profession").first()
    if resident:
        return str(resident.fullname), resident.profession
    return "", ""
