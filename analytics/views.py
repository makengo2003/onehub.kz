from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from . import services


@api_view(["GET"])
def get_analytics(request: Request) -> Response:
    starts_at = request.query_params.get("starts_at")
    ends_at = request.query_params.get("ends_at")

    if not starts_at or not ends_at:
        return Response({"error": "starts_at and ends_at arguments are required."})

    booking_requests_analytics = services.get_booking_requests_analytics(starts_at, ends_at)
    booked_places_analytics = services.get_booked_places_analytics(starts_at, ends_at)
    residents_analytics = services.get_residents_analytics(starts_at, ends_at)
    return Response({"booking_requests_analytics": booking_requests_analytics,
                     "booked_places_analytics": booked_places_analytics,
                     "residents_analytics": residents_analytics})
