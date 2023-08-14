from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.core.serializers import serialize
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.test import APIClient

from booking.models import BookedPlace, BookingRequest, AcceptedBookingRequest
from project.utils import datetime_now


class BookedPlaceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(User.objects.create_user('u', 'p', is_staff=True, is_superuser=True))
        self.base_booked_place_data = {
            "consumer_fullname": "TestCase",
            "consumer_phone_number": "+77779185334",
            "starts_at": datetime.now(),
            "deposit": 1000,
            "is_paid": True,
            "payment_type": "cash",
            "number": "A1",
            "type": "open_space_fixed_place",
            "duration": 1,
            "term": "hours",
            "time_type": "daytime"
        }

    def _add_booked_place_case_201(self, booking_request_id=None):
        before_count = BookedPlace.objects.all().count()

        self.base_booked_place_data["booking_request_id"] = booking_request_id
        response = self.client.post(reverse("add_booked_place"), self.base_booked_place_data, format="json")

        before_count += 1
        self.assertEqual(BookedPlace.objects.all().count(), before_count)
        self.assertEqual(response.data, {"success": True, "message": "Created"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        if booking_request_id:
            booked_place = BookedPlace.objects.all().order_by("-id")[0]
            booking_request = BookingRequest.objects.get(id=booking_request_id)
            self.assertEqual(booking_request.is_accepted, True)
            self.assertEqual(booking_request.answered_at.date(), datetime_now().date())
            self.assertEqual(
                AcceptedBookingRequest.objects.filter(booking_request_id=booking_request.id,
                                                      booked_place_id=booked_place.id).exists(), True)

    def _booking_request_to_booked_place_case(self):
        BookedPlace.objects.all().delete()
        booking_request = BookingRequest.objects.create(consumer_fullname="TestCase",
                                                        consumer_phone_number="+77779185334")
        self._add_booked_place_case_201(booking_request_id=booking_request.id)

    def _add_booked_place_case_409(self):
        before_count = BookedPlace.objects.all().count()
        response = self.client.post(reverse("add_booked_place"), self.base_booked_place_data, format="json")

        self.assertEqual(BookedPlace.objects.all().count(), before_count)
        self.assertEqual(response.data, {"success": False, "message": "Place is not free at given datetime"})
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def _add_booked_place_case_400(self):
        response = self.client.post(reverse("add_booked_place"), format="json")
        self.assertEqual(response.data, {"success": False, "message": "Bad Request"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_booked_place_view(self):
        self._add_booked_place_case_201()
        self._booking_request_to_booked_place_case()
        self._add_booked_place_case_409()
        self._add_booked_place_case_400()

    def _renew_booked_place_case_201(self):
        self._add_booked_place_case_201()

        url = reverse("renew_booked_place")
        data = {
            "booked_place_id": 1,
            "duration": 2,
            "term": "hours",
            "time_type": "daytime",
        }

        before_expires_at = BookedPlace.objects.get(id=1).expires_at
        response = self.client.post(url, data, format="json")
        after_expires_at = BookedPlace.objects.get(id=1).expires_at

        self.assertEqual(after_expires_at.replace(second=0, microsecond=0),
                         (before_expires_at + relativedelta(hours=2)).replace(second=0, microsecond=0))
        self.assertEqual(response.data, {"success": True, "message": "OK"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _renew_booked_place_case_409(self):
        self.base_booked_place_data["starts_at"] = datetime.now() - relativedelta(hours=1)
        self._add_booked_place_case_201()

        url = reverse("renew_booked_place")
        data = {
            "booked_place_id": 2,
            "duration": 2,
            "term": "hours",
            "time_type": "daytime",
        }

        before_expires_at = BookedPlace.objects.get(id=2).expires_at
        response = self.client.post(url, data, format="json")
        after_expires_at = BookedPlace.objects.get(id=2).expires_at

        self.assertEqual(after_expires_at, before_expires_at)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data, {"success": False, "message": "Place is not free at given datetime"})

    def _renew_booked_place_case_400(self):
        response = self.client.post(reverse("renew_booked_place"), format="json")

        self.assertEqual(response.data, {"success": False, "message": "Bad Request"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_renew_booked_place_view(self):
        self._renew_booked_place_case_201()
        self._renew_booked_place_case_409()
        self._renew_booked_place_case_400()

    def test_delete_booked_place_view(self):
        self._add_booked_place_case_201()

        booked_place = BookedPlace.objects.all()[0]
        url = reverse("delete_booked_place")
        data = {"booked_place_id": booked_place.id}

        before_status = booked_place.status
        response = self.client.post(url, data, format="json")

        current_status = BookedPlace.objects.all()[0].status
        self.assertNotEqual(before_status, current_status)
        self.assertEqual(current_status, "deleted")
        self.assertEqual(response.data, {"success": True})

    def test_update_booked_place_info_view(self):
        self._add_booked_place_case_201()

        booked_place = BookedPlace.objects.all()[0]
        url = reverse("update_booked_place_info")
        data = {
            "booked_place_id": booked_place.id,
            "field_for_updating": "duration",
            "new_value": 2
        }

        before_value = booked_place.duration
        response = self.client.post(url, data, format="json")

        current_value = BookedPlace.objects.all()[0].duration
        self.assertNotEqual(before_value, current_value)
        self.assertEqual(current_value, 2)
        self.assertEqual(response.data, {"success": True})

    def test_get_booked_places_list_view(self):
        data = {
            "last_obj_id": 0
        }
        url = reverse("get_booked_places_list")

        response = self.client.get(url, data, format="json")
        self.assertEqual(response.data, {"booked_places_list": serialize("json", []), "last_obj_id": None})

        self._add_booked_place_case_201()

        response = self.client.get(url, data, format="json")
        self.assertEqual(response.data, {"booked_places_list": serialize("json", BookedPlace.objects.all()),
                                         "last_obj_id": 1})

    def test_get_deleted_booked_places_list_view(self):
        self._add_booked_place_case_201()

        data = {
            "last_obj_id": 0
        }
        url = reverse("get_deleted_booked_places_list")

        response = self.client.get(url, data, format="json")
        self.assertEqual(response.data, {"deleted_booked_places_list": serialize("json", []), "last_obj_id": None})

        booked_place = BookedPlace.objects.all()[0]
        booked_place.status = "deleted"
        booked_place.save(update_fields=["status"])

        response = self.client.get(url, data, format="json")
        self.assertEqual(response.data, {"deleted_booked_places_list": serialize("json", BookedPlace.objects.all()),
                                         "last_obj_id": 1})
