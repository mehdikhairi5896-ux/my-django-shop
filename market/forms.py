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

        labels = {
            "title": "عنوان کالا",
            "description": "توضیحات کالا",
            "price": "قیمت",
            "city": "شهر",
            "image": "عکس کالا",
        }

        widgets = {
            "price": forms.TextInput(
                attrs={
                    "inputmode": "numeric",
                    "placeholder": "مثلاً 5,000,000",
                }
            ),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        return price
