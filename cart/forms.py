from django import forms
import re


class OrderForm(forms.Form):
    phone = forms.CharField(
        max_length=20,
        label="شماره موبایل",
        widget=forms.TextInput(attrs={
            "placeholder": "مثال: 09123456789"
        })
    )

    address = forms.CharField(
        label="آدرس ارسال",
        widget=forms.Textarea(attrs={
            "placeholder": "آدرس دقیق خود را وارد کنید..."
        })
    )

def clean_phone(self):
    phone = self.cleaned_data["phone"].strip()

    # تبدیل اعداد فارسی و عربی به انگلیسی
    phone = phone.translate(str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789"
    ))

    if not re.fullmatch(r"09\d{9}", phone):
        raise forms.ValidationError(
            "لطفاً یک شماره موبایل معتبر وارد کنید."
        )

    return phone
