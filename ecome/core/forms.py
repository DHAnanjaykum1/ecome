from dataclasses import fields
from .models import Address
from tkinter import Widget

from django import forms 

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder' : "Promo Code",
}))

class CheckoutForm(forms.ModelForm):
    class Meta:
        model  = Address
        exclude = ["user",]
