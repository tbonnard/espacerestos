from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('event/', views.event_create, name='event_create'),
    path('event/<int:event_id>', views.event_details, name='event_details'),
    path('event_edit/<int:event_id>', views.event_edit, name='event_edit'),
    path('location/', views.location_create, name='location_create'),
    path('location/<int:location_id>', views.location_details, name='location_details'),
    path('location_edit/<int:location_id>', views.location_edit, name='location_edit'),
    path('logout/', views.logout_view, name='logout_view'),
]