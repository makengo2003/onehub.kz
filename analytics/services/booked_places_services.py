from typing import Mapping
from django.db.models import QuerySet

from analytics import main_services


def get_booked_places_analytics(period_label: str, booked_places: QuerySet[Mapping]) -> Mapping:
    place_types = {}
    time_types = {}
    terms = {}
    total_booked_places_count = {}
    became_resident_count = {}

    for booked_place in booked_places:
        place_types[booked_place["type"]] = place_types.get(booked_place["type"], 0) + 1
        time_types[booked_place["time_type"]] = time_types.get(booked_place["time_type"], 0) + 1
        terms[booked_place["term"]] = terms.get(booked_place["term"], 0) + 1

        label = main_services.get_period_label(period_label, booked_place["created_at"])

        total_booked_places_count[label] = total_booked_places_count.get(label, 0) + 1
        if booked_place["from_booked_place_to_resident"]:
            became_resident_count[label] = became_resident_count.get(label, 0) + 1

    return {
        "booked_places_count": {
            "labels": total_booked_places_count.keys(),
            "datasets": [
                {
                    "label": f"Общая кол. {sum(total_booked_places_count.values())}",
                    "data": total_booked_places_count.values()
                },
                {
                    "label": f"Стал резидентом {sum(became_resident_count.values())}",
                    "data": became_resident_count.values()
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
            ],
        },
        "terms": {
            "labels": terms.keys(),
            "datasets": [
                {
                    "label": "Количество",
                    "data": terms.values()
                }
            ],
        },
        "time_types": {
            "labels": time_types.keys(),
            "datasets": [
                {
                    "label": "Количество",
                    "data": time_types.values()
                }
            ],
        },
    }
