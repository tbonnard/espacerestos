from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Location, Event


class UserAdminCustom(admin.ModelAdmin):
    list_display = ('username', 'user_type', 'email')


class LocationAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Location._meta.get_fields()]
    list_display = ("name","address", "address_2", "address_number", "city", "zip_code", "country", "manager_location" )


class EventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Event._meta.get_fields()]


admin.site.register(User, UserAdminCustom)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)