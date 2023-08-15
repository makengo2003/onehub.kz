from datetime import datetime
from typing import Mapping, Tuple

from dateutil.relativedelta import relativedelta
from django.db.models import Q, Count

from booking.models import BookingRequest, BookedPlace
from project.utils import datetime_now
from resident.models import Resident
from .services import booking_requests_services, booked_places_services, residents_services


def get_booking_requests_analytics(period_label: str, starts_at: datetime, ends_at: datetime) -> Mapping:
    booking_requests = BookingRequest.objects.filter(
        Q(created_at__gte=starts_at) & Q(created_at__lte=ends_at)
    ).select_related("rejected_booking_request").order_by('created_at').values(
        "rejected_booking_request__rejection_reason",
        "place_type", "created_at", "is_accepted")

    return booking_requests_services.get_booking_requests_analytics(period_label, booking_requests)


def get_booked_places_analytics(period_label: str, starts_at: datetime, ends_at: datetime) -> Mapping:
    booked_places = BookedPlace.objects.filter(
        Q(created_at__gte=starts_at) & Q(created_at__lte=ends_at)
    ).select_related("from_booked_place_to_resident").order_by('created_at').values("created_at", "type", "term",
                                                                                    "time_type", "deposit",
                                                                                    "payment_type", "is_paid",
                                                                                    "from_booked_place_to_resident")

    return booked_places_services.get_booked_places_analytics(period_label, booked_places)


def get_residents_analytics(period_label: str, starts_at: datetime, ends_at: datetime) -> Mapping:
    residents = Resident.objects.filter(
        Q(created_at__gte=starts_at) & Q(created_at__lte=ends_at)
    ).select_related("visited_days").order_by('created_at').annotate(visited_times=Count("visited_days")).values(
        "created_at", "place_type", "term", "time_type", "profession",
        "price", "payment_type", "duration", "visited_times")

    return residents_services.get_residents_analytics(period_label, residents)


periods = {
    "today": {
        "starts_at": datetime_now().replace(hour=0, minute=0),
        "ends_at": datetime_now().replace(hour=23, minute=59)
    },
    "yesterday": {
        "starts_at": datetime_now().replace(hour=0, minute=0) - relativedelta(days=1),
        "ends_at": datetime_now().replace(hour=23, minute=59) - relativedelta(days=1)
    },
    "week_ago": {
        "starts_at": datetime_now().replace(hour=0, minute=0) - relativedelta(weeks=1),
        "ends_at": datetime_now().replace(hour=23, minute=59)
    },
    "month_ago": {
        "starts_at": datetime_now().replace(hour=0, minute=0) - relativedelta(months=1),
        "ends_at": datetime_now().replace(hour=23, minute=59)
    },
    "year_ago": {
        "starts_at": datetime_now().replace(hour=0, minute=0) - relativedelta(years=1),
        "ends_at": datetime_now().replace(hour=23, minute=59)
    }
}


def get_starts_and_ends_at_dt_from_period_label(period_label: str) -> Tuple[datetime, datetime]:
    return periods[period_label]["starts_at"], periods[period_label]["ends_at"]


month_names = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь"
}


def get_period_label(period_label: str, dt: datetime) -> str:
    if period_label == "today" or period_label == "yesterday":
        label = f'Время: {str(dt.hour)}:00'
    elif period_label == "week_ago":
        label = f'{month_names[dt.month]}: {str(dt.day)}'
    elif period_label == "month_ago":
        label = f'{month_names[dt.month]}: {str(dt.day)}'
    else:
        label = month_names[dt.month]

    return label
