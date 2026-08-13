from django import forms
from .models import MarketItem


class MarketItemForm(forms.ModelForm):
    class Meta:
        model = MarketItem
        fields = [
            "title",
            "description",
            "price",
            "city",
            "image",
        ]
