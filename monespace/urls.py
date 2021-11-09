from django.urls import path
from . import views, views_login

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views_login.login_view, name='login_view'),
    path('register/', views_login.register, name='register'),
    path('logout/', views_login.logout_view, name='logout_view'),
    path('profil/', views.profile, name='profile'),
    path('event/', views.event_create, name='event_create'),
    path('event/<int:event_id>', views.event_details, name='event_details'),
    path('event_edit/<int:event_id>', views.event_edit, name='event_edit'),
    path('events/', views.events_list_date, name='events_list_date'),
    path('benevoles/<int:location_id>', views.users_site, name='users_site'),
    path('location/', views.location_create, name='location_create'),
    path('locations/', views.locations, name='locations'),
    path('select_locations/', views_login.select_locations, name='select_locations'),
    path('location/<int:location_id>', views.location_details, name='location_details'),
    path('location_edit/<int:location_id>', views.location_edit, name='location_edit'),
]

