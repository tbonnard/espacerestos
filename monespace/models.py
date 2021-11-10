from django.db import models
from django.contrib.auth.models import AbstractUser
from django import utils


class User(AbstractUser):
    user_type_choices = ((1, 'Admin'), (2, 'User'), (3, 'Manager'))
    user_type = models.IntegerField(choices=user_type_choices, null=False, blank=False, default=2)
    # location = models.ForeignKey("Location", on_delete=models.SET_NULL, null=True, blank=True, related_name="users_locations")


class Location(models.Model):
    name = models.CharField(blank=False, max_length=255)
    address = models.CharField(blank=False, max_length=255)
    address_2 = models.CharField(blank=True, max_length=255, default="")
    address_number = models.IntegerField(blank=False)
    city = models.CharField(blank=False, max_length=255)
    zip_code = models.CharField( blank=False, max_length=5)
    country_list = (("FR", 'France'), ("CA", 'Canada'))
    country = models.CharField(choices=country_list, blank=False, max_length=2)
    # manager_location = models.ForeignKey(User, limit_choices_to={'user_type':3}, on_delete=models.SET_NULL, null=True, blank=False, related_name="location_manager")
    manager_location = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name="location_manager")
    # users = models.ManyToManyField(User) ==> legacy -- use of a new table: StatusUsersLocations

    def __str__(self):
        return self.name


class Event(models.Model):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=False, related_name="events_locations")
    name = models.CharField( blank=False, max_length=255)
    description = models.TextField(blank=True, default="")
    start_date = models.DateField( blank=False, default=utils.timezone.now)
    end_date = models.DateField( blank=True, null=True)
    time_from = models.TimeField(blank=True, default="00:00:00")
    time_to = models.TimeField(blank=True, default="00:00:00")
    is_recurring = models.BooleanField(default=False)
    is_full_day = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name} - {self.pk}"


class RecurringPattern(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=True)
    separation_count = models.IntegerField(blank=True, null=True)
    repeat_each_x = models.IntegerField(blank=True, null=True)
    # day_of_week = models.IntegerField(blank=True, null=True)
    # week_of_month = models.IntegerField(blank=True, null=True)
    # day_of_month = models.IntegerField(blank=True, null=True)
    # month_of_year = models.IntegerField(blank=True, null=True)
    max_num_occurrences = models.IntegerField(blank=True, null=True)

#https://vertabelo.com/blog/again-and-again-managing-recurring-events-in-a-data-model/


class EventExceptionCancelledRescheduled(models.Model):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=False, related_name="events_exceptions_locations")
    name = models.CharField( blank=False, max_length=255)
    description = models.TextField(blank=True, default="")
    start_date = models.DateField( blank=False, default=utils.timezone.now)
    end_date = models.DateField( blank=True, null=True)
    time_from = models.TimeField(blank=True, default="00:00:00")
    time_to = models.TimeField(blank=True, default="00:00:00")
    is_cancelled = models.BooleanField(default=False)
    is_rescheduled = models.BooleanField(default=False)
    is_full_day = models.BooleanField(default=False)
    parent_event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=True)


class AttendeesEvents(models.Model):
    parent_event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    status = models.IntegerField(blank=False, null=False, default=0)


class StatusUsersLocations(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False, null=False,
                                 related_name="location_status_user")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False,
                             related_name="user_status_location")
    status_choices = ((1, 'En attente'), (2, 'Actif'), (3, 'Rejeté'), (4, 'Désactivé'), (5, "Annulé par l'utilisateur"))
    status = models.IntegerField(choices=status_choices, null=False, blank=False, default=1)

    def __str__(self):
        return f"{self.user} - {self.location} - {self.status}"

    def __repr__(self):
        return f"{self.user} - {self.location} - {self.status}"
