import json
from typing import Mapping

from django.db.models import QuerySet

from site_settings.models import CarouselImage


def get_carousel_images() -> QuerySet[CarouselImage]:
    return CarouselImage.objects.all().order_by("serial_number")


def save_carousel_images(form_data: Mapping, files: Mapping) -> None:
    CarouselImage.objects.all().delete()

    images = json.loads(form_data["images"])
    orm_images = list()

    for i, image in enumerate(images):
        img = files.get(str(i+1) + ". " + image["name"], False)

        if not img:
            img = image['url'][image['url'][1:].index("/") + 1:]

        orm_images.append(CarouselImage(name=image["name"], serial_number=image["serial_number"],
                                        image=img))

    CarouselImage.objects.bulk_create(orm_images)
