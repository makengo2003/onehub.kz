from project import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view

from booking.services import booked_place_services as booking_services


@api_view(["POST"])
def add_booked_place_view(request):
    print(settings.request_user)
    success, status_code, message = booking_services.add_booked_place(request.data)
    return Response({"success": success, "message": message}, status=status_code)


@api_view(["POST"])
def renew_booked_place_view(request):
    success, status_code, message = booking_services.renew_booked_place(request.data)
    return Response({"success": success, "message": message}, status=status_code)


@api_view(["POST"])
def delete_booked_place_view(request):
    booked_place_id = request.data.get("booked_place_id")
    booking_services.delete_booked_place(booked_place_id)
    return Response({"success": True})


@api_view(["POST"])
def update_booked_place_info_view(request):
    booked_place_id = request.data.get("booked_place_id")
    field_for_updating = request.data.get("field_for_updating")
    new_value = request.data.get("new_value")
    booking_services.update_booked_place_info(booked_place_id, field_for_updating, new_value)
    return Response({"success": True})


@api_view(["GET"])
def search_by_fullname_view(request):
    fullname = request.query_params.get("fullname")
    phone_number = booking_services.search_by_fullname(fullname)
    return Response({"phone_number": phone_number})


@api_view(["GET"])
def search_by_phone_number_view(request):
    phone_number = request.query_params.get("phone_number")
    fullname = booking_services.search_by_phone_number(phone_number)
    return Response({"fullname": fullname})
