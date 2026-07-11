from django import forms

class OrderForm(forms.Form):
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
