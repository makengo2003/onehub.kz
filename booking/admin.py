from django.contrib import admin
from .models import *


admin.site.register(BookedPlace)
admin.site.register(BookingRequest)
admin.site.register(FromBookedPlaceToResident)
admin.site.register(RejectedBookingRequest)
admin.site.register(AcceptedBookingRequest)
