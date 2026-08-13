from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = [
            "donor_name",
            "amount",
            "description",
        ]

        labels = {
            "donor_name": "نام کمک‌کننده",
            "amount": "مبلغ کمک",
            "description": "توضیحات",
        }

        widgets = {
            "donor_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "amount": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control"
            }),
        }
