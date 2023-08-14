from django.urls import path
from .views.booking_request_notification_views import *
from .views.carousel_images_views import *
from .views.price_setting_views import *


urlpatterns = [
    path("get_booking_request_notification_emails/", get_booking_request_notification_emails_view,
         name="get_booking_request_notification_emails"),
    path("save_booking_request_notification_emails/", save_booking_request_notification_emails_view,
         name="save_booking_request_notification_emails"),
    path("get_carousel_images/", get_carousel_images_view, name="get_carousel_images"),
    path("save_carousel_images/", save_carousel_images_view, name="save_carousel_images"),
    path("get_prices_of_place_type/", get_prices_of_place_type_view,
         name="get_prices_of_place_type"),
    path("add_place_type/", add_place_type_view, name="add_place_type"),
    path("delete_place_type/", delete_place_type_view, name="delete_place_type"),
    path("update_place_type_info_and_its_prices/", update_place_type_info_and_its_prices_view,
         name="update_place_type_info_and_its_prices"),
    path("get_place_types/", get_place_types_view, name="get_place_types"),
]
