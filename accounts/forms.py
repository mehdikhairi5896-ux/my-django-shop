from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']

        labels = {
            'image': 'عکس پروفایل',
            'bio': 'درباره من',
        }

        widgets = {
            'image': forms.FileInput(attrs={
                'accept': 'image/*',
            }),
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'مثلاً: سلام، من مهدی هستم و به برنامه‌نویسی علاقه دارم.',
            }),
        }
