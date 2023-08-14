from django import forms
from booking.models import BookingRequest


class LeaveBookingRequestForm(forms.ModelForm):
    place_type = forms.CharField(required=False)

    class Meta:
        model = BookingRequest
        fields = ['consumer_fullname', 'consumer_phone_number', 'place_type']
