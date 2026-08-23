from django import forms
from .models import Advertisement


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = [
            "title",
            "description",
            "city",
            "image",
            "duration",
            "price",
        ]

        widgets = {
            "price": forms.TextInput(
                attrs={
                    "inputmode": "numeric",
                    "placeholder": "مثلاً 12,000,000",
                }
            ),
        }
