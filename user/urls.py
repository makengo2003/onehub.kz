from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *


urlpatterns = [
    path("", main_page_view, name="main_page"),
    path("dogovor-oferta/", dogovor_oferta_page_view, name="dogovor_oferta_page"),
    path("leave_booking_request/", leave_booking_request_view, name="leave_booking_request"),
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]
