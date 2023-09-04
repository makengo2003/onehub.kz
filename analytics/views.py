from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from . import main_services as services


@api_view(["GET"])
def get_analytics(request: Request) -> Response:
    starts_at = datetime.strptime(request.query_params.get("starts_at"), "%Y-%m-%d")
    ends_at = datetime.strptime(request.query_params.get("ends_at"), "%Y-%m-%d")

    period_label = services.get_period_name(starts_at, ends_at)

    booking_requests_analytics = services.get_booking_requests_analytics(period_label, starts_at, ends_at)
    booked_places_analytics = services.get_booked_places_analytics(period_label, starts_at, ends_at)
    residents_analytics = services.get_residents_analytics(period_label, starts_at, ends_at)
    return Response({"booking_requests_analytics": booking_requests_analytics,
                     "booked_places_analytics": booked_places_analytics,
                     "residents_analytics": residents_analytics})
