from django.contrib.auth.decorators import user_passes_test
from django.http import FileResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from project import settings
from .services import *
from django.views.decorators.cache import never_cache


@never_cache
def admin_page_view(request):
    if request.user.is_superuser or request.user.is_staff:
        return render(request, "admin_page.html", {"terms": settings.PLACE_BOOKING_TERMS})
    return redirect("/")


@api_view(["POST"])
def change_username_and_password_view(request):
    change_username_and_password(request, request.user, request.data)
    return Response({"success": True})


@api_view(["GET"])
def get_residents_list_view(request):
    residents_list, last_obj_id = get_residents_list(request.query_params.get("last_obj_id", 0))
    return Response({"residents_list": residents_list, "last_obj_id": last_obj_id})


@api_view(["GET"])
def get_deleted_residents_list_view(request):
    deleted_residents_list, last_obj_id = get_deleted_residents_list(request.query_params.get("last_obj_id", 0))
    return Response({"deleted_residents_list": serialize("python", deleted_residents_list), "last_obj_id": last_obj_id})


@api_view(["GET"])
def get_booked_places_list_view(request):
    booked_places_list, last_obj_id = get_booked_places_list(request.query_params.get("last_obj_id", 0))
    return Response({"booked_places_list": serialize("python", booked_places_list), "last_obj_id": last_obj_id})


@api_view(["GET"])
def get_deleted_booked_places_list_view(request):
    deleted_booked_places_list, last_obj_id = get_deleted_booked_places_list(request.query_params.get("last_obj_id", 0))
    return Response({"deleted_booked_places_list": serialize("python", deleted_booked_places_list),
                     "last_obj_id": last_obj_id})


@api_view(["GET"])
def get_booking_requests_list_view(request):
    booking_requests_list, last_obj_id = get_booking_requests_list(request.query_params.get("last_obj_id", 0))
    return Response({"booking_requests_list": serialize("python", booking_requests_list), "last_obj_id": last_obj_id})


@user_passes_test(lambda user: user.is_superuser)
def export_to_excel_2months_view(_):
    excel_file_path = export_to_excel_2months()
    return FileResponse(open(excel_file_path, "rb"))


@user_passes_test(lambda user: user.is_superuser)
def export_to_excel_daily_view(_):
    excel_file_path = export_to_excel_daily()
    return FileResponse(open(excel_file_path, "rb"))
