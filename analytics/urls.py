from django.urls import path
from .views import get_analytics


urlpatterns = [
    path("get_analytics/", get_analytics, name="get_analytics")
]
