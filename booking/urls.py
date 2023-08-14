from django.urls import path
from booking.views.booking_request_views import *
from booking.views.booked_place_views import *


urlpatterns = [
    path("get_new_booking_requests_count/", get_new_booking_requests_count_view, name="get_new_booking_requests_count"),
    path("make_booking_request_rejected/", make_booking_request_rejected_view, name="make_booking_request_rejected"),
    path("add_booked_place/", add_booked_place_view, name="add_booked_place"),
    path("renew_booked_place/", renew_booked_place_view, name="renew_booked_place"),
    path("delete_booked_place/", delete_booked_place_view, name="delete_booked_place"),
    path("update_booked_place_info/", update_booked_place_info_view, name="update_booked_place_info"),
    path("search_by_fullname/", search_by_fullname_view, name="search_by_fullname"),
    path("search_by_phone_number/", search_by_phone_number_view, name="search_by_phone_number"),
]
