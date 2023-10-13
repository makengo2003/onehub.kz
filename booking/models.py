from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from project import settings
from project.utils import datetime_now
from resident.models import Resident


class BookedPlace(models.Model):
    consumer_fullname = models.CharField(max_length=255)
    consumer_phone_number = PhoneNumberField()
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime_now, editable=False)
    status = models.CharField(max_length=100, choices=settings.PLACE_STATUSES, default="active")
    deposit = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=50, choices=settings.PAYMENT_TYPES)
    number = models.CharField(max_length=10, null=True, blank=True)
    type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    term = models.CharField(max_length=50, choices=settings.PLACE_BOOKING_TERMS)
    time_type = models.CharField(max_length=50, choices=settings.TIME_TYPES)
    discount = models.PositiveIntegerField(null=True, blank=True, default=0)
    price = models.PositiveIntegerField(default=0)
    window = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.pk}. {self.consumer_fullname} [{str(self.status).upper()}]. {self.created_at}"


class FromBookedPlaceToResident(models.Model):
    booked_place = models.OneToOneField(BookedPlace, on_delete=models.CASCADE,
                                        related_name="from_booked_place_to_resident")
    resident = models.OneToOneField(Resident, on_delete=models.CASCADE,
                                    related_name="from_booked_place_to_resident")
    created_at = models.DateTimeField(default=datetime_now, editable=False)

    def __str__(self):
        return f"BOOKED_PLACE_ID: {self.booked_place_id} RESIDENT_ID: {self.resident_id} DATE: {self.created_at}. {self.created_at}"


class BookingRequest(models.Model):
    consumer_fullname = models.CharField(max_length=255)
    consumer_phone_number = PhoneNumberField()
    place_type = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime_now, editable=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    is_accepted = models.BooleanField(null=True, blank=True)

    def __str__(self):
        status = "not answered" if self.is_accepted is None else "accepted" if self.is_accepted else "rejected"
        return f"{self.pk}. {self.consumer_fullname} [{status}]. {self.created_at}"


class RejectedBookingRequest(models.Model):
    booking_request = models.OneToOneField(BookingRequest, on_delete=models.CASCADE,
                                           related_name="rejected_booking_request")
    rejection_reason = models.TextField()
    created_at = models.DateTimeField(default=datetime_now, editable=False)

    def __str__(self):
        return f"{self.pk}. REJECTION REASON: {self.rejection_reason}. {self.created_at}"


class AcceptedBookingRequest(models.Model):
    booking_request = models.OneToOneField(BookingRequest, on_delete=models.CASCADE,
                                           related_name="accepted_booking_request")
    booked_place = models.OneToOneField(BookedPlace, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime_now, editable=False)

    def __str__(self):
        return f"{self.pk}. BOOKING_REQUEST_ID: {self.booking_request_id} BOOKED_PLACE_ID: {self.booked_place_id}. {self.created_at}"
