from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models.base import Model
from django import forms

from .models import User, Event, Location


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")


class UserAuthenticationForm(AuthenticationForm):
    pass


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        # fields = ('transaction_type', 'quantity')
        widgets = {
            "date": forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            "time_from": forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'hh:mm'}),
            "time_to": forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'hh:mm'}),
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
#         fields = ("name", "address", "address_2", "address_number", "city", "zip_code", "country", "manager_location")


