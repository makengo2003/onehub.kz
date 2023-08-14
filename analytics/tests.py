from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from booking.models import BookingRequest


# class AnalyticsTest(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.client.force_authenticate(User.objects.create_user('u', 'p', is_staff=True, is_superuser=True))
#
#     def _get_booking_requests_analytics_case(self, response):
#         print(response.data)
#         self.assertEqual(True, True)
#
#     def _prepare_test_booking_requests_data(self):
#         booking_requests = []
#
#         for i in range(100):
#             BookingRequest.objects.create(consumer_fullname="FIO",
#                                           consumer_phone_number="+77779185334",
#                                           place_type="Open Space",
#                                           answered_at=,
#                                           is_accepted=i % 2)
#
#         BookingRequest.objects.bulk_create()
#
#     def test_get_analytics(self):
#         self._prepare_test_booking_requests_data()
#         now = datetime.now()
#         before_now = now - relativedelta(months=1)
#
#         response = self.client.get(reverse("get_analytics"), {"starts_at": before_now, "ends_at": now}, format="json")
#         self._get_booking_requests_analytics_case(response)
