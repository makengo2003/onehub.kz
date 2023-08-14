from booking.models import BookingRequest, RejectedBookingRequest
from project.utils import datetime_now


def get_new_booking_requests_count() -> int:
    return BookingRequest.objects.filter(answered_at=None).count()


def make_booking_request_rejected(booking_request_id: int, rejection_reason: str) -> None:
    BookingRequest.objects.filter(id=booking_request_id).update(is_accepted=False, answered_at=datetime_now())
    RejectedBookingRequest.objects.create(booking_request_id=booking_request_id, rejection_reason=rejection_reason)
