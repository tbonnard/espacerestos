from django.urls import path
from . import views, views_login, views_events, views_locations, views_download, views_attend

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views_login.login_view, name='login_view'),
    path('register/', views_login.register, name='register'),
    path('logout/', views_login.logout_view, name='logout_view'),
    path('profil/', views.profile, name='profile'),
    path('benevoles_site/<int:location_id>', views.users_site, name='users_site'),
    path('benevoles/', views.all_users_site, name='all_users_site'),
    path('benevoles_status/<int:location_id>', views.user_site_update_status, name='user_site_update_status'),
    path('event/', views_events.event_create, name='event_create'),
    path('event/<int:event_id>', views_events.event_details, name='event_details'),
    path('event_edit/<int:event_id>', views_events.event_edit, name='event_edit'),
    path('events/', views_events.events_list_date, name='events_list_date'),
    path('event_delete_all/<int:event_id>', views_events.event_delete_all, name='event_delete_all'),
    path('event_delete_rec/<int:event_id>', views_events.event_delete_rec, name='event_delete_rec'),
    path('location/', views_locations.location_create, name='location_create'),
    path('locations/', views_locations.locations, name='locations'),
    path('select_locations/', views_locations.select_locations, name='select_locations'),
    path('location/<int:location_id>', views_locations.location_details, name='location_details'),
    path('location_edit/<int:location_id>', views_locations.location_edit, name='location_edit'),
    path('download_users_csv/', views_download.download_users_csv, name='download_users_csv'),
    path('api_get_specific_attendees/', views_attend.api_get_specific_attendees, name='api_get_specific_attendees'),
    path('api_get_all_attendees_user/', views_attend.api_get_all_attendees_user, name='api_get_all_attendees_user'),
    path('api_attend_decline_event/', views_attend.api_attend_decline_event, name='api_attend_decline_event'),

]

