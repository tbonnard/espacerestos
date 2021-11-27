from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User, Event, Location, RecurringPattern, StatusUsersLocations, AttendeesEvents


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")


class UserAuthenticationForm(AuthenticationForm):
    pass


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('location', "name", "description", "start_date", "end_date", "time_from", "time_to", "is_full_day", "is_recurring")

        widgets = {
            "start_date": forms.SelectDateWidget(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            "end_date": forms.SelectDateWidget(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
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
        # fields = '__all__'
        fields = ("name", "address", "address_2", "address_number", "city", "zip_code", "country", "manager_location")


class SelectLocationsForm(forms.Form):
    locations = forms.ModelMultipleChoiceField(queryset=Location.objects.all(), required=True)


class StatusUsersLocationsForm(forms.ModelForm):
    class Meta:
        model = StatusUsersLocations
        fields = ('status',)


class AttendeesEventsForm(forms.ModelForm):
    class Meta:
        model = AttendeesEvents
        fields= ('plus_other',)
