from django.urls import path
from .views.resident_views import *


urlpatterns = [
    path("calculate_resident_adding_price/", calculate_resident_adding_price_view,
         name="calculate_resident_adding_price"),
    path("calculate_resident_renewing_price/", calculate_resident_renewing_price_view,
         name="calculate_resident_renewing_price"),
    path("add_resident/", add_resident_view, name="add_resident"),
    path("renew_resident/", renew_resident_view, name="renew_resident"),
    path("delete_resident/", delete_resident_view, name="delete_resident"),
    path("update_resident_info/", update_resident_info_view, name="update_resident_info"),
    path("update_resident_visited_today_status/", update_resident_visited_today_status_view,
         name="update_resident_visited_today_status"),
    path("get_attendance_of_resident/", get_attendance_of_resident_view, name="get_attendance_of_resident"),
    path("search_by_fullname/", search_by_fullname_view, name="search_by_fullname"),
    path("search_by_phone_number/", search_by_phone_number_view, name="search_by_phone_number"),
]
