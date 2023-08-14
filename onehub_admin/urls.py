from django.urls import path
from .views import *


urlpatterns = [
    path("change_username_and_password/", change_username_and_password_view,
         name="change_username_and_password"),
    path("get_residents_list/", get_residents_list_view, name="get_residents_list"),
    path("get_deleted_residents_list/", get_deleted_residents_list_view, name="get_deleted_residents_list"),
    path("get_booked_places_list/", get_booked_places_list_view, name="get_booked_places_list"),
    path("get_deleted_booked_places_list/", get_deleted_booked_places_list_view, name="get_deleted_booked_places_list"),
    path("get_booking_requests_list/", get_booking_requests_list_view, name="get_booking_requests_list"),
    path("export_to_excel_2months/", export_to_excel_2months_view, name="export_to_excel_2months"),
    path("export_to_excel_daily/", export_to_excel_daily_view, name="export_to_excel_daily"),
]
