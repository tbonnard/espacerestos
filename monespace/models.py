from django.db import models
from django.contrib.auth.models import AbstractUser
from django import utils


class User(AbstractUser):
    user_type_choices = ((1, 'Admin'), (2, 'User'), (3, 'Manager'))
    user_type = models.IntegerField(choices=user_type_choices, null=False, blank=False, default=2)
    location = models.ForeignKey("Location", on_delete=models.SET_NULL, null=True, blank=True, related_name="users_locations")


class Location(models.Model):
    name = models.CharField(blank=False, max_length=255)
    address = models.CharField(blank=False, max_length=255)
    address_2 = models.CharField(blank=True, max_length=255, default="")
    address_number = models.IntegerField(blank=False)
    city = models.CharField(blank=False, max_length=255)
    zip_code = models.CharField( blank=False, max_length=5)
    country_list = (("FR", 'France'), ("CA", 'Canada'))
    country = models.CharField(choices=country_list, blank=False, max_length=2)
    manager_location = models.ForeignKey(User, limit_choices_to={'user_type':3}, on_delete=models.SET_NULL, null=True, blank=False, related_name="location_manager")

    def __str__(self):
        return self.name


class Event(models.Model):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=False, related_name="events_locations")
    name = models.CharField( blank=False, max_length=255)
    description = models.TextField(blank=True, default="")
    date = models.DateField( blank=False, default=utils.timezone.now)
    time_from = models.TimeField(blank=True, default="00:00:00")
    time_to = models.TimeField(blank=True, default="00:00:00")

    def __str__(self):
        return self.name


