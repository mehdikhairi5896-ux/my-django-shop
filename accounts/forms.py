from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileForm(forms.ModelForm):

    image = forms.ImageField(
    label="تصویر پروفایل",
    required=False,
    widget=forms.FileInput(attrs={
        "accept": "image/*"
    })
)
    bio = forms.CharField(
        label="درباره من",
        required=False,
        widget=forms.Textarea(attrs={
            "placeholder": "درباره خودت بنویس...",
            "rows": 5,
        })
    )

    class Meta:
        model = Profile
        fields = ["image", "bio"]

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError("رمزهای عبور یکسان نیستند.")

        return password2
