from django.urls import path
from .views import get_admin_actions_view


urlpatterns = [
    path("get_admin_actions/", get_admin_actions_view, name="get_admin_actions")
]
