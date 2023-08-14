from django import forms
from .models import Resident


class AddResidentForm(forms.ModelForm):
    booked_place_id = forms.IntegerField(required=False)
    place_number = forms.CharField(max_length=10, required=False)

    class Meta:
        model = Resident
        exclude = ("deleted_at", "expires_at", "status", "price", "paper_count")


class RenewResidentForm(forms.ModelForm):
    resident_id = forms.IntegerField(required=True)

    class Meta:
        model = Resident
        fields = ("payment_type", "duration", "term", "time_type", "used_discount")
