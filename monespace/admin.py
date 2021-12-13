from django.contrib import admin

from .models import User, Location, Event, RecurringPattern, StatusUsersLocations, LogsStatusUsersLocations, \
    EventExceptionCancelledRescheduled, AttendeesEvents


class UserAdminCustom(admin.ModelAdmin):
    list_display = ('uuid', "username", 'email', 'user_type', 'date_joined')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('uuid', "name", "address", "address_2", "city", "zip_code", "country", 'created')


class EventAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'location', 'name', 'event_manager', 'start_date', 'is_recurring', 'is_distrib', 'is_cancelled', 'created')


class RecurringPatternAdmin(admin.ModelAdmin):
    list_display = ('event', "separation_count", "max_num_occurrences", 'created')


class StatusUsersLocationsAdmin(admin.ModelAdmin):
    list_display = ('location', 'distrib',  "user", 'status', 'created', 'modified')


class LogsStatusUsersLocationsAdmin(admin.ModelAdmin):
    list_display = ('location', 'distrib', 'from_user', "user", 'status', 'current_status', 'created')


class EventExceptionCancelledRescheduledAdmin(admin.ModelAdmin):
    list_display=('location', 'parent_event', 'start_date', 'is_cancelled', 'is_rescheduled')


class AttendeesEventsAdmin(admin.ModelAdmin):
    list_display = ('parent_event', 'user', 'status', 'event_date', 'plus_other')


admin.site.register(User, UserAdminCustom)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(RecurringPattern, RecurringPatternAdmin)
admin.site.register(StatusUsersLocations, StatusUsersLocationsAdmin)
admin.site.register(LogsStatusUsersLocations, LogsStatusUsersLocationsAdmin)
admin.site.register(EventExceptionCancelledRescheduled, EventExceptionCancelledRescheduledAdmin)
admin.site.register(AttendeesEvents, AttendeesEventsAdmin)

