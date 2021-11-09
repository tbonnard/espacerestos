from django.urls import path
from . import views, views_login, views_events, views_locations

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views_login.login_view, name='login_view'),
    path('register/', views_login.register, name='register'),
    path('logout/', views_login.logout_view, name='logout_view'),
    path('profil/', views.profile, name='profile'),
    path('benevoles/<int:location_id>', views.users_site, name='users_site'),
    path('event/', views_events.event_create, name='event_create'),
    path('event/<int:event_id>', views_events.event_details, name='event_details'),
    path('event_edit/<int:event_id>', views_events.event_edit, name='event_edit'),
    path('events/', views_events.events_list_date, name='events_list_date'),
    path('location/', views_locations.location_create, name='location_create'),
    path('locations/', views_locations.locations, name='locations'),
    path('select_locations/', views_locations.select_locations, name='select_locations'),
    path('location/<int:location_id>', views_locations.location_details, name='location_details'),
    path('location_edit/<int:location_id>', views_locations.location_edit, name='location_edit'),
]

