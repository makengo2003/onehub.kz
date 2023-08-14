from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from rest_framework.decorators import permission_classes, api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from site_settings.models import CarouselImage, PlaceTypePrice
from .services import *


@never_cache
def main_page_view(request):
    prices = PlaceTypePrice.objects.all().select_related("place_type")
    place_types = dict()

    for price in prices:
        if place_types.get(price.place_type.name):
            place_types[price.place_type.name].append(price)
        else:
            place_types[price.place_type.name] = [price]

    return render(request, "main_page.html", {"carousel_images": CarouselImage.objects.all(),
                                              "place_types": place_types})


@never_cache
def dogovor_oferta_page_view(request):
    return render(request, "dogovor-oferta.html")


@api_view(["POST"])
@parser_classes([MultiPartParser])
@permission_classes([AllowAny])
def leave_booking_request_view(request):
    booking_request, success = leave_booking_request(request.data)

    if success:
        notify_administrators_of_booking_request(booking_request)

    return Response({"success": success})


def login_view(request):
    logged_in = user_login(request)
    if logged_in:
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

