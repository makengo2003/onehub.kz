from typing import Mapping
from django.db.models import Min, Max, Avg, F, QuerySet


def get_booking_requests_analytics(period_label: str, booking_requests: QuerySet[Mapping]) -> Mapping:
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

        if period_label == "today" or period_label == "yesterday":
            label = f'Время: {str(booking_request["created_at"].hour)}:00'
        elif period_label == "week_ago":
            label = f'День: {str(booking_request["created_at"].day)}'
        elif period_label == "month_ago":
            label = f'День: {str(booking_request["created_at"].day)}'
        else:
            label = f'Месяц: {str(booking_request["created_at"].month)}'

        if booking_request["is_accepted"]:
            accepted_booking_requests_count[label] = accepted_booking_requests_count.get(label, 0) + 1
        else:
            rejected_booking_requests_count[label] = rejected_booking_requests_count.get(label, 0) + 1

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

    return {
        "booking_requests_count": {
            "labels": accepted_booking_requests_count.keys(),
            "datasets": [
                {
                    "label": f'Принято (Общ. {sum(accepted_booking_requests_count.values())})',
                    "data": accepted_booking_requests_count.values(),
                },
                {
                    "label": f'Отказано (Общ. {sum(rejected_booking_requests_count.values())})',
                    "data": rejected_booking_requests_count.values(),
                }
            ]
        },
        "place_types": {
            "labels": place_types.keys(),
            "datasets": [
                {
                    "label": "Количество",
                    "data": place_types.values()
                }
            ]
        },

        "rejection_reasons_list": rejection_reasons_list,
        "response_times": response_times,
        "booking_requests_total_count": total_booking_requests_count
    }
