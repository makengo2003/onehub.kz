from django.core.serializers import serialize
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from booking.models import BookingRequest, RejectedBookingRequest
from project.utils import datetime_now


class BookingRequestTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(User.objects.create_user('u', 'p', is_staff=True, is_superuser=True))
        self.booking_request = BookingRequest.objects.create(consumer_fullname="TestCase",
                                                             consumer_phone_number="+77779185334",
                                                             place_type="open_space_fixed_place")

    def test_get_new_booking_requests_count_view(self):
        response = self.client.get(reverse("get_new_booking_requests_count"), format="json")

        current_count = BookingRequest.objects.filter(answered_at=None).count()
        self.assertEqual(current_count, response.data["new_booking_requests_count"])

        BookingRequest.objects.create(consumer_fullname="TestCase",
                                      consumer_phone_number="+77779185334",
                                      place_type="open_space_fixed_place")

        response = self.client.get(reverse("get_new_booking_requests_count"), format="json")
        self.assertEqual(current_count + 1, response.data["new_booking_requests_count"])

    def test_make_booking_request_rejected_view(self):
        data = {
            "booking_request_id": self.booking_request.id,
            "rejection_reason": "some rejection reason"
        }
        url = reverse("make_booking_request_rejected")
        booking_request = BookingRequest.objects.get(id=self.booking_request.id)

        self.assertEqual(booking_request.is_accepted, None)
        self.assertEqual(booking_request.answered_at, None)

        response = self.client.post(url, data, format="json")

        booking_request = BookingRequest.objects.get(id=self.booking_request.id)
        self.assertEqual(booking_request.is_accepted, False)
        self.assertEqual(booking_request.answered_at.date(), datetime_now().date())
        rejected_booking_request_exists = RejectedBookingRequest.objects.filter(
            booking_request=booking_request,
            rejection_reason="some rejection reason").exists()
        self.assertEqual(rejected_booking_request_exists, True)
        self.assertEqual(response.data, {"success": True})

    def test_get_booking_requests_list_view(self):
        data = {
            "last_obj_id": 0
        }
        url = reverse("get_booking_requests_list")

        response = self.client.get(url, data, format="json")
        self.assertEqual(response.data, {"booking_requests_list": serialize("json", [self.booking_request]),
                                         "last_obj_id": 1})

        self.booking_request.delete()

        response = self.client.get(url, data, format="json")
        self.assertEqual(response.data, {"booking_requests_list": serialize("json", []), "last_obj_id": None})
