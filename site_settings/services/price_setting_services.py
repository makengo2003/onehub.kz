from typing import Mapping

from project import settings
from django.db.models import QuerySet

from admin_actions.models import AdminAction
from site_settings.models import PlaceTypePrice, PlaceType


def get_prices_of_place_type(place_type_id: int) -> QuerySet[PlaceTypePrice]:
    return PlaceTypePrice.objects.filter(place_type_id=place_type_id)


def add_place_type(place_type_name: str) -> PlaceType:
    return PlaceType.objects.create(name=place_type_name)


def delete_place_type(place_type_id: int) -> None:
    PlaceType.objects.filter(id=place_type_id).delete()


def update_place_type_info_and_its_prices(form_data: Mapping) -> None:
    place_type_id = form_data.get("id")
    place_type = PlaceType.objects.filter(id=place_type_id).first()
    place_type.name = form_data.get("name")
    place_type.save(update_fields=["name"])

    orm_prices = list()
    for price in form_data.get("prices"):
        orm_prices.append(PlaceTypePrice(place_type_id=place_type_id, **price))

    PlaceTypePrice.objects.filter(place_type_id=place_type_id).delete()
    PlaceTypePrice.objects.bulk_create(orm_prices)

    request_user = getattr(settings, 'request_user', None)
    AdminAction.objects.create(admin_fullname=request_user.username,
                               title=f"Изменил тарифы для тип места {place_type.name}")


def get_place_types() -> QuerySet[PlaceType]:
    return PlaceType.objects.all()
