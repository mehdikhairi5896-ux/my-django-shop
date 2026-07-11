from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2*1024*1024:  # حداکثر حجم ۲ مگابایت
                raise forms.ValidationError("حجم تصویر نباید بیش از ۲ مگابایت باشد.")
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("فرمت تصویر باید JPEG یا PNG باشد.")
        return image
