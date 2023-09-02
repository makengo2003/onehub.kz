from project import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from project.utils import datetime_now


class Resident(models.Model):
    fullname = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    profession = models.CharField(max_length=255)

    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime_now, editable=False)

    status = models.CharField(max_length=100, choices=settings.PLACE_STATUSES, default="active")
    used_discount = models.PositiveIntegerField(null=True, blank=True, default=0)
    price = models.IntegerField()
    payment_type = models.CharField(max_length=50, choices=settings.PAYMENT_TYPES)

    place_number = models.CharField(max_length=10, null=True, blank=True)
    place_type = models.CharField(max_length=100)
    paper_count = models.IntegerField(null=True, blank=True, default=0)
    duration = models.PositiveIntegerField()
    term = models.CharField(max_length=50, choices=settings.PLACE_BOOKING_TERMS)
    time_type = models.CharField(max_length=50, choices=settings.TIME_TYPES)

    locker = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.pk}. {self.fullname} [{str(self.status).upper()}]. {self.created_at}"


class ResidentVisitedDay(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="visited_days")
    date = models.DateField(default=datetime_now)

    def __str__(self):
        return f"{self.pk}. RESIDENT_ID: {self.resident_id} DATE: {self.date}"


# TODO: class ResidentsLocker(models.Model):
#     resident_fullname = models.CharField(max_length=255)
#     resident_phone_number = PhoneNumberField()
#     starts_at = models.DateTimeField()
#     expires_at = models.DateTimeField()
#     deleted_at = models.DateTimeField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=100, choices=settings.LOCKER_STATUSES, default="active")
#     price = models.IntegerField(default=settings.PRICE_FOR_LOCKER)
#     payment_type = models.CharField(max_length=50, choices=settings.PAYMENT_TYPES)
#     locker_number = models.CharField(max_length=10)
#     def __str__(self):
#         return f"{self.pk}. {self.resident_fullname} [{str(self.status).upper()}]"
