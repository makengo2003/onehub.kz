from django import forms
from .models import BookedPlace


class AddBookedPlaceForm(forms.ModelForm):
    booking_request_id = forms.IntegerField(required=False)

    class Meta:
        model = BookedPlace
        exclude = ("expires_at", "deleted_at", "status", "price")


class RenewBookedPlaceForm(forms.ModelForm):
    booked_place_id = forms.IntegerField(required=True)

    class Meta:
        model = BookedPlace
        fields = ("duration", "term", "time_type", "discount", "window")
