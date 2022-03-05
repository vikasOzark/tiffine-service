from django import forms
from .models import AddressModel


class Address(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields = ['street', 'locality', 'landmark', 'city', 'pincode']
