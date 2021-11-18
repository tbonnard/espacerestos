from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .models import Location, StatusUsersLocations, LogsStatusUsersLocations, User, AttendeesEvents
from .views_events import events_list
from .forms import StatusUsersLocationsForm
from .functions_global import get_date_to

from datetime import date


@property
def is_past_due(self):
    return date.today() > self.date


@login_required(login_url='/login/')
def index(request):
    date_to = get_date_to()

    if request.user.user_type == 1:
        user_locations = Location.objects.all()
    else:
        user_locations_pre = StatusUsersLocations.objects.filter(user=request.user, status=1) | \
                         StatusUsersLocations.objects.filter(user=request.user, status=2)
        user_locations = [i.location for i in user_locations_pre]

    eligible_events_date_locations = events_list(date_from=None, date_to=None, location=user_locations)

    pending_location = []
    if StatusUsersLocations.objects.filter(user=request.user, status=1):
        pending_location = [i.location for i in StatusUsersLocations.objects.filter(user=request.user, status=1)]

    attendees = AttendeesEvents.objects.filter(user=request.user)

    return render(request, 'index.html', context={"events": eligible_events_date_locations, "date_to": date_to, "pending_location":pending_location, "attendees":attendees})


@login_required(login_url='/login/')
def all_users_site(request):
    if request.user.user_type != 1:
        return redirect('index')
    users = User.objects.all()
    form = StatusUsersLocationsForm()
    status_users_location = StatusUsersLocations.objects.filter(status=1) | StatusUsersLocations.objects.filter(status=2)
    return render(request, 'benevoles.html', context={"status_users_location": status_users_location, "form": form, "users":users})


@login_required(login_url='/login/')
def users_site(request, location_id):
    if request.user.user_type == 2:
        return redirect('index')
    elif request.user.user_type == 3 and Location.objects.get(pk=location_id) not in Location.objects.filter(manager_location=request.user):
        return redirect('index')
    else:
        status_users_location = StatusUsersLocations.objects.filter(location=Location.objects.get(pk=location_id),
                                                                    status=1) | StatusUsersLocations.objects.filter(
            location=Location.objects.get(pk=location_id), status=2)
        form = StatusUsersLocationsForm()
        if request.method == "POST":
            try:
                user_status_update = StatusUsersLocations.objects.get(pk=request.GET['id'])
            except:
                pass
            else:
                user_status_update.status = 2
                user_status_update.save()
                logs = LogsStatusUsersLocations(location=user_status_update.location, from_user=request.user, user=user_status_update.user, status=2, current_status=user_status_update.status)
                logs.save()
                return redirect(reverse('users_site', kwargs={'location_id': location_id}))
        return render(request, 'benevoles_site.html', context={'location_id': location_id, "status_users_location": status_users_location, "form": form})


@login_required(login_url='/login/')
def user_site_update_status(request, location_id):
    if request.user.user_type == 2:
        return redirect('index')
    else:
        if request.method == "POST":
            try:
                user_status_update = StatusUsersLocations.objects.get(pk=request.GET['id'])
            except:
                pass
            else:
                user_status_update.status = request.POST['status']
                user_status_update.save()
                logs = LogsStatusUsersLocations(location=user_status_update.location, from_user=request.user, user=user_status_update.user, status=request.POST['status'], current_status=user_status_update.status)
                logs.save()
                return redirect(reverse('users_site', kwargs={'location_id': location_id}))


@login_required(login_url='/login/')
def profile(request):
    date_to = get_date_to()
    user_locations_pre = StatusUsersLocations.objects.filter(user=request.user, status=1) | StatusUsersLocations.objects.filter(user=request.user, status=2)
    user_locations = [i.location for i in user_locations_pre]
    user_manager_locations = Location.objects.filter(manager_location=request.user)
    return render(request, 'profile.html', context={'locations': user_locations, "date_to":date_to, 'manager_locations': user_manager_locations})
