from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework.response import Response

from site_settings.services.price_setting_services import *


@api_view(["GET"])
def get_prices_of_place_type_view(request):
    place_types_with_their_prices = get_prices_of_place_type(request.query_params.get("place_type_id"))
    return Response({"prices": serialize("python", place_types_with_their_prices)})


@api_view(["POST"])
def add_place_type_view(request):
    place_type = add_place_type(request.data.get("place_type_name"))
    return Response({"success": True, "id": place_type.id})


@api_view(["POST"])
def delete_place_type_view(request):
    delete_place_type(request.data.get("place_type_id"))
    return Response({"success": True})


@api_view(["POST"])
def update_place_type_info_and_its_prices_view(request):
    update_place_type_info_and_its_prices(request.data)
    return Response({"success": True})


@api_view(["GET"])
def get_place_types_view(_):
    place_types = get_place_types()
    return Response({"place_types": serialize("python", place_types)})
