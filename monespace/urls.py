from django.urls import path
from . import views, views_login, views_events, views_locations, views_download, views_attend
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views_login.login_view, name='login_view'),
    path('register/', views_login.register, name='register'),
    path('logout/', views_login.logout_view, name='logout_view'),
    path('faq/', views.faq_view, name='faq'),
    path('profil/', views.profile, name='profile'),
    path('profil_edit/', views.profile_edit, name='profile_edit'),
    path('benevoles_site/<int:location_id>', views.users_site, name='users_site'),
    path('benevoles/', views.all_users_site, name='all_users_site'),
    path('benevoles_status/<int:location_id>', views.user_site_update_status, name='user_site_update_status'),
    path('event/', views_events.event_create, name='event_create'),
    path('event/<int:event_id>', views_events.event_details, name='event_details'),
    path('event_edit/<int:event_id>', views_events.event_edit, name='event_edit'),
    path('event_edit_one/<int:event_id>', views_events.event_edit_specific_rec, name='event_edit_specific_rec'),
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
    path('api_get_count_specific_attendees/', views_attend.api_get_count_specific_attendees, name='api_get_count_specific_attendees'),
    path('api_get_all_attendees_user/', views_attend.api_get_all_attendees_user, name='api_get_all_attendees_user'),
    path('api_attend_decline_event/', views_attend.api_attend_decline_event, name='api_attend_decline_event'),

    # Change Password
    path('change-password/', auth_views.PasswordChangeView.as_view(
            template_name='commons/change_password.html',
            success_url='/'
        ), name='change_password'),

    # Forget Password
    path('password-reset/', auth_views.PasswordResetView.as_view(
             template_name='commons/password_reset/password_reset.html',
             subject_template_name='commons/password_reset/password_reset_subject.txt',
             email_template_name='commons/password_reset/password_reset_email.html',
             # success_url='/login/'
         ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
             template_name='commons/password_reset/password_reset_done.html'
         ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
             template_name='commons/password_reset/password_reset_confirm.html'
         ), name='password_reset_confirm'),
    path('password-reset-complete/',  auth_views.PasswordResetCompleteView.as_view(
             template_name='commons/password_reset/password_reset_complete.html'
         ), name='password_reset_complete'),

]

