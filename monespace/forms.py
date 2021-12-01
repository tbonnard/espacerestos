from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User, Event, Location, RecurringPattern, StatusUsersLocations, AttendeesEvents


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "email", 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", 'last_name', "email", "address", "city", "zip_code", "tel", "profile_picture")
        widgets = {
            "profile_picture": forms.FileInput(),
            "email":forms.EmailInput(),
        }
        labels = {
            "first_name": "Prénom",
            'last_name': "Nom",
            "email": "Email",
            "address": "Adresse",
            "city":"Ville",
            "zip_code": "Code Postal",
            "tel":"Téléphone pour vous joindre",
            "profile_picture": "Photo de profil"
        }


class UserAuthenticationForm(AuthenticationForm):
    pass


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('location', "name", "description", "start_date", "end_date", "is_full_day", "time_from", "time_to", "is_recurring")
        widgets = {
            "start_date":forms.DateInput(attrs={'type': 'date'}),
            "end_date": forms.DateInput(attrs={'type': 'date'}),
            "time_from": forms.TimeInput(attrs={'type': 'time'}),
            "time_to": forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            "location": "Site de l'événement",
            "name": "Nom de l'événement",
            "description": "Description",
            "start_date": "Date de début",
            "end_date": "Date de fin",
                "time_from": "Heure de début",
                    "time_to": "Heure de fin",
                    "is_full_day": "L'événement dure toute la journée",
            "is_recurring": "L'événement se répète"
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
            "max_num_occurrences": "pendant... fois (en plus de celui ci)"
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        # fields = '__all__'
        fields = ("name", "address", "address_2", "city", "zip_code", "country", "manager_location")
        labels = {
            "name":"Nom du site",
            "address": "Adresse",
            "address_2": "Complément d'adresse",
            "city": "Ville",
            "zip_code": "Code postal",
                    "country": "Pays",
            "manager_location": "Gestionnaire du site"
        }


class SelectLocationsForm(forms.Form):
    locations = forms.ModelMultipleChoiceField(Location.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)


class StatusUsersLocationsForm(forms.ModelForm):
    class Meta:
        model = StatusUsersLocations
        fields = ('status',)


class AttendeesEventsForm(forms.ModelForm):
    class Meta:
        model = AttendeesEvents
        fields = ('plus_other',)
