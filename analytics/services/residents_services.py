from typing import Mapping
from analytics import main_services
from django.db.models import QuerySet


def get_residents_analytics(period_label: str, residents: QuerySet[Mapping]) -> Mapping:
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
        label = main_services.get_period_label(period_label, resident["created_at"])

        residents_count[label] = residents_count.get(label, 0) + 1
        income[label] = income.get(label, 0) + resident["price"]

        income_grouped_by_payment_type[resident["payment_type"]] = income_grouped_by_payment_type.get(
            resident["payment_type"], 0) + resident["price"]

        place_types[resident["place_type"]] = place_types.get(resident["place_type"], 0) + 1

        terms[resident["term"]] = terms.get(resident["term"], 0) + 1

        time_types[resident["time_type"]] = time_types.get(resident["time_type"], 0) + 1

        professions.append(resident["profession"])

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

    return {
        "residents_count": {
            "labels": residents_count.keys(),
            "datasets": [
                {
                    "label": f"Количество (Общ. {sum(residents_count.values())})",
                    "data": residents_count.values()
                }
            ]
        },
        "place_types": {
            "labels": place_types.keys(),
            "datasets": [
                {
                    "label": "Тип места",
                    "data": place_types.values()
                }
            ]
        },
        "terms": {
            "labels": terms.keys(),
            "datasets": [
                {
                    "label": "Показатель по срокам",
                    "data": terms.values()
                }
            ]
        },
        "time_types": {
            "labels": time_types.keys(),
            "datasets": [
                {
                    "label": "Время дня",
                    "data": time_types.values()
                }
            ]
        },
        "income": {
            "labels": income.keys(),
            "datasets": [
                {
                    "label": f"Доход (Общ. {sum(income.values())})",
                    "data": income.values()
                }
            ]
        },
        "income_grouped_by_payment_type": {
            "labels": income_grouped_by_payment_type.keys(),
            "datasets": [
                {
                    "label": "Тг",
                    "data": income_grouped_by_payment_type.values()
                }
            ]
        },
        "residents_day_visiting": {
            "labels": ["Ожидалось", "На самом деле пришли"],
            "datasets": [
                {
                    "label": "Количество посещаемости",
                    "data": [residents_visiting["day"]["Отсутствие"], residents_visiting["day"]["Присутствие"]],
                },
            ]
        },
        "residents_nighttime_visiting": {
            "labels": ["Ожидалось", "На самом деле пришли"],
            "datasets": [
                {
                    "label": "Количество посещаемости",
                    "data": [residents_visiting["nighttime"]["Отсутствие"], residents_visiting["nighttime"]["Присутствие"]],
                },
            ]
        },
        "residents_daytime_visiting": {
            "labels": ["Ожидалось", "На самом деле пришли"],
            "datasets": [
                {
                    "label": "Количество посещаемости",
                    "data": [residents_visiting["daytime"]["Отсутствие"], residents_visiting["daytime"]["Присутствие"]],
                },
            ]
        },

        "professions": professions,
        "total_visiting_hours": total_visiting_hours
    }
