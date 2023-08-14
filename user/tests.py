from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from booking.models import BookingRequest


class UserAppTest(TestCase):
    def leave_booking_request_fail_test(self):
        booking_requests_count = BookingRequest.objects.count()
        data = {
            "guess_fullname": "Guess Fullname",
            "guess_phone_number": "+7777918533",
            "place_type": "not_found_place_type"
        }
        url = reverse("user:leave_booking_request")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(booking_requests_count, BookingRequest.objects.count())

    def leave_booking_request_pass_test(self):
        booking_requests_count = BookingRequest.objects.count()
        data = {
            "guess_fullname": "Guess Fullname",
            "guess_phone_number": "+77779185334",
            "place_type": "open_space_not_fixed_place"
        }
        url = reverse("user:leave_booking_request")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(booking_requests_count + 1, BookingRequest.objects.count())

    def user_login_fail_test(self):
        pass

    def user_login_pass_test(self):
        self.client.logout()
