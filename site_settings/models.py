from django.db import models
from project import settings


class CarouselImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="carousel_images/")
    serial_number = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.serial_number}. {self.image.url}"


class BookingRequestNotificationEmail(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class PlaceType(models.Model):
    name = models.CharField(max_length=100)


class PlaceTypePrice(models.Model):
    place_type = models.ForeignKey(PlaceType, on_delete=models.CASCADE, related_name="prices")
    duration = models.PositiveIntegerField()
    term = models.CharField(max_length=50, choices=settings.PLACE_BOOKING_TERMS)
    time_type = models.CharField(max_length=50, choices=settings.TIME_TYPES)
    price = models.IntegerField()
