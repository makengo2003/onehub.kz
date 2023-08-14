from rest_framework.decorators import api_view
from rest_framework.response import Response

from booking.services import booking_request_services


@api_view(["GET"])
def get_new_booking_requests_count_view(_):
    new_booking_requests_count = booking_request_services.get_new_booking_requests_count()
    return Response({"new_booking_requests_count": new_booking_requests_count})


@api_view(["POST"])
def make_booking_request_rejected_view(request):
    booking_request_id = request.data.get("booking_request_id")
    rejection_reason = request.data.get("rejection_reason")
    booking_request_services.make_booking_request_rejected(booking_request_id, rejection_reason)
    return Response({"success": True})
