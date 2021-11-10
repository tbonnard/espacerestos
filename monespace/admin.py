from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Location, Event, RecurringPattern, StatusUsersLocations


class UserAdminCustom(admin.ModelAdmin):
    list_display = ('username', 'user_type', 'email', 'date_joined')


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "address_2", "address_number", "city", "zip_code", "country", "manager_location", 'created')


class EventAdmin(admin.ModelAdmin):
    list_display = ('location', 'name', 'start_date', 'is_recurring', 'created')


class RecurringPatternAdmin(admin.ModelAdmin):
    list_display = ('event', "separation_count", 'created')


class StatusUsersLocationsAdmin(admin.ModelAdmin):
    list_display = ('location', "user", 'status', 'created', 'modified')


admin.site.register(User, UserAdminCustom)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(RecurringPattern, RecurringPatternAdmin)
admin.site.register(StatusUsersLocations, StatusUsersLocationsAdmin)
