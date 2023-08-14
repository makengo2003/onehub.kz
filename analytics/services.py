from datetime import datetime
from typing import Mapping

from django.db.models import Q, F, Min, Max, Avg, Count

from booking.models import BookingRequest, BookedPlace
from resident.models import Resident


def get_booking_requests_analytics(starts_at: datetime, ends_at: datetime) -> Mapping:
    booking_requests = BookingRequest.objects.filter(
        Q(created_at__gte=starts_at) & Q(created_at__lte=ends_at)
    ).select_related("rejected_booking_request").values(
        "rejected_booking_request__rejection_reason",
        "place_type", "created_at", "is_accepted")

    rejection_reasons_list = []
    accepted_booking_requests_count = {}
    rejected_booking_requests_count = {}
    total_booking_requests_count = {}
    place_types = {}

    for booking_request in booking_requests:
        place_types[booking_request["place_type"]] = place_types.get(booking_request["place_type"], 0) + 1

        if booking_request["rejected_booking_request__rejection_reason"]:
            rejection_reasons_list.append(booking_request["rejected_booking_request__rejection_reason"])

        created_at_date = booking_request["created_at"].date()
        total_booking_requests_count[created_at_date.year] = total_booking_requests_count.get(created_at_date.year, {})
        total_booking_requests_count[created_at_date.year][created_at_date.month - 1] = \
            total_booking_requests_count[created_at_date.year].get(created_at_date.month - 1, 0) + 1

        if booking_request["is_accepted"]:
            accepted_booking_requests_count[created_at_date.year] = \
                accepted_booking_requests_count.get(created_at_date.year, {})
            accepted_booking_requests_count[created_at_date.year][created_at_date.month - 1] = \
                accepted_booking_requests_count[created_at_date.year].get(created_at_date.month - 1, 0) + 1
        else:
            rejected_booking_requests_count[created_at_date.year] = \
                rejected_booking_requests_count.get(created_at_date.year, {})
            rejected_booking_requests_count[created_at_date.year][created_at_date.month - 1] = \
                rejected_booking_requests_count[created_at_date.year].get(created_at_date.month - 1, 0) + 1

    booking_requests_count = {
        "accepted": accepted_booking_requests_count,
        "rejected": rejected_booking_requests_count,
        "total": total_booking_requests_count
    }

    booking_requests = booking_requests.aggregate(
        min_response_time=Min(F("answered_at") - F("created_at")),
        max_response_time=Max(F("answered_at") - F("created_at")),
        avg_response_time=Avg(F("answered_at") - F("created_at"))
    )

    response_times = {
        "min": -1,
        "max": -1,
        "avg": -1
    }

    if booking_requests["min_response_time"]:
        response_times["min"] = booking_requests["min_response_time"].seconds // 60
    if booking_requests["max_response_time"]:
        response_times["max"] = booking_requests["max_response_time"].seconds // 60
    if booking_requests["avg_response_time"]:
        response_times["avg"] = booking_requests["avg_response_time"].seconds // 60

    return {"booking_requests_count": booking_requests_count, "place_types": place_types,
            "rejection_reasons_list": rejection_reasons_list, "response_times": response_times}


def get_booked_places_analytics(starts_at: datetime, ends_at: datetime) -> Mapping:
    booked_places = BookedPlace.objects.filter(
        Q(created_at__gte=starts_at) & Q(created_at__lte=ends_at)
    ).select_related("from_booked_place_to_resident").values("created_at", "type", "term", "time_type", "deposit",
                                                             "payment_type", "is_paid", "from_booked_place_to_resident")

    place_types = {}
    time_types = {}
    terms = {}
    deposits = {}
    total_booked_places_count = {}
    became_resident_count = {}
    deposits_grouped_by_payment_type = {}

    for booked_place in booked_places:
        place_types[booked_place["type"]] = place_types.get(booked_place["type"], 0) + 1
        time_types[booked_place["time_type"]] = time_types.get(booked_place["time_type"], 0) + 1
        terms[booked_place["term"]] = terms.get(booked_place["term"], 0) + 1

        created_at_date = booked_place["created_at"].date()
        total_booked_places_count[created_at_date.year] = total_booked_places_count.get(created_at_date.year, {})
        total_booked_places_count[created_at_date.year][created_at_date.month - 1] = \
            total_booked_places_count[created_at_date.year].get(created_at_date.month - 1, 0) + 1

        if booked_place["from_booked_place_to_resident"]:
            became_resident_count[created_at_date.year] = became_resident_count.get(created_at_date.year, {})
            became_resident_count[created_at_date.year][created_at_date.month - 1] = \
                became_resident_count[created_at_date.year].get(created_at_date.month - 1, 0) + 1
        if booked_place["is_paid"]:
            deposits[created_at_date.year] = deposits.get(created_at_date.year, {})
            deposits[created_at_date.year][created_at_date.month - 1] = \
                deposits[created_at_date.year].get(created_at_date.month - 1, 0) + booked_place["deposit"]

            deposits_grouped_by_payment_type[booked_place["payment_type"]] = deposits_grouped_by_payment_type.get(
                booked_place["payment_type"], 0) + booked_place["deposit"]

    booked_places_count = {
        "total": total_booked_places_count,
        "became_resident_count": became_resident_count
    }

    return {"booked_places_count": booked_places_count, "place_types": place_types,
            "terms": terms, "time_types": time_types, "deposits": {"total": deposits},
            "deposits_grouped_by_payment_type": deposits_grouped_by_payment_type}


def get_residents_analytics(starts_at: datetime, ends_at: datetime) -> Mapping:
    residents = Resident.objects.filter(
        Q(created_at__gte=starts_at) & Q(created_at__lte=ends_at)
    ).select_related("visited_days").annotate(visited_times=Count("visited_days")).values(
        "created_at", "place_type", "term", "time_type", "profession",
        "price", "payment_type", "duration", "visited_times")

    residents_count = {}
    place_types = {}
    terms = {}
    time_types = {}
    professions = []
    income = {}
    income_grouped_by_payment_type = {}
    total_visiting_hours = 0
    residents_visiting = {"daytime": {"Отсутствие": 0, "Присутствие": 0},
                          "nighttime": {"Отсутствие": 0, "Присутствие": 0},
                          "day": {"Отсутствие": 0, "Присутствие": 0}}

    for resident in residents:
        created_at_date = resident["created_at"].date()
        residents_count[created_at_date.year] = residents_count.get(created_at_date.year, {})
        residents_count[created_at_date.year][created_at_date.month - 1] = residents_count[created_at_date.year].get(
            created_at_date.month - 1, 0) + 1
        place_types[resident["place_type"]] = place_types.get(resident["place_type"], 0) + 1
        terms[resident["term"]] = terms.get(resident["term"], 0) + 1
        time_types[resident["time_type"]] = time_types.get(resident["time_type"], 0) + 1
        professions.append(resident["profession"])
        income[created_at_date.year] = income.get(created_at_date.year, {})
        income[created_at_date.year][created_at_date.month - 1] = income[created_at_date.year].get(
            created_at_date.month - 1, 0) + resident["price"]
        income_grouped_by_payment_type[resident["payment_type"]] = income_grouped_by_payment_type.get(
            resident["payment_type"], 0) + resident["price"]

        if resident["term"] == "hours" or (resident["term"] == "days" and resident["duration"] == 1):
            residents_visiting[resident["time_type"]]["Отсутствие"] = residents_visiting.get(
                resident["time_type"]).get("Отсутствие", 0) + 1
        else:
            expected_visiting_times = 1 if resident["term"] == "days" else 7 if resident["term"] == "weeks" else 30
            residents_visiting[resident["time_type"]]["Отсутствие"] = residents_visiting.get(
                resident["time_type"]).get("Отсутствие", 0) + (expected_visiting_times * resident["duration"])

        residents_visiting[resident["time_type"]]["Присутствие"] = residents_visiting[resident["time_type"]].get(
            "Присутствие", 0) + resident["visited_times"]

        if resident["term"] == "hours":
            if resident["visited_times"] > 0:
                total_visiting_hours += resident["duration"]
        else:
            if resident["time_type"] == "day":
                time_type = 24
            elif resident["time_type"] == "daytime":
                time_type = 14
            else:
                time_type = 10

            total_visiting_hours += resident["visited_times"] * time_type

    for time_type in residents_visiting.keys():
        residents_visiting[time_type]["Отсутствие"] -= residents_visiting[time_type]["Присутствие"]

    return {"residents_count": {"total": residents_count}, "place_types": place_types, "terms": terms,
            "time_types": time_types, "professions": professions, "income": {"total": income},
            "income_grouped_by_payment_type": income_grouped_by_payment_type, "residents_visiting": residents_visiting,
            "total_visiting_hours": total_visiting_hours}
