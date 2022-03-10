from django import forms
from .models import AddressModel
from django.forms import ModelForm, Textarea


class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields = ('street', 'locality', 'landmark', 'city', 'pincode')
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control', 'id': 'street-id'}),
            'locality': forms.TextInput(attrs={'class': 'form-control', 'id': 'locality-id'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control', 'id': 'landmark-id'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city-id'}),
            'pincode': forms.NumberInput(attrs={'class': 'form-control', 'id': 'pincode-id'}),
        }
