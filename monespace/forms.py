from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models.base import Model
from django import forms
import json
from .models import User, Event, Location, RecurringPattern


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
            "start_date": forms.SelectDateWidget(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            "time_from": forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'hh:mm'}),
            "time_to": forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'hh:mm'}),
        }


class EventRecurringPatternForm(forms.ModelForm):
    class Meta:
        model = RecurringPattern
        repeat_each_x_choices = ((0, 'semaine'), (1, 'jour'), (2, 'mois'), (3, 'trimestre'),
                                (4, 'semestre'), (5, 'année'))
        day_of_week_choices = ((0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'), (3, 'Jeudi'), (4, 'Vendredi'),
                               (5, 'Samedi'), (6, 'Dimanche'))
        # fields = ('separation_count', "repeat_each_x", "max_num_occurrences", "day_of_week", "week_of_month",
        #           "day_of_month", "month_of_year" )
        fields = ('separation_count', "repeat_each_x", "max_num_occurrences")
        widgets = {
            "day_of_week": forms.RadioSelect(choices=day_of_week_choices),
            "repeat_each_x": forms.Select(choices=repeat_each_x_choices),
        }

        labels = {
            "day_of_week": "le",
            'separation_count': 'répéter tous/toutes les',
            'repeat_each_x': '',
            "max_num_occurrences": "le répéter en plus du celui ci pendant... fois"
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
#         fields = ("name", "address", "address_2", "address_number", "city", "zip_code", "country", "manager_location")


