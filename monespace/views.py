from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
import datetime

from .models import Location, StatusUsersLocations
from .views_events import events_list
from .forms import StatusUsersLocationsForm


def get_date_to():
    weeks = 8
    days_added = datetime.timedelta(weeks=weeks)
    date_to = (datetime.datetime.now() + days_added).strftime("%Y-%m-%d")
    return date_to


@login_required(login_url='/login/')
def index(request):
    date_to = get_date_to()

    #user_locations = Location.objects.filter(users=request.user)
    user_locations_pre = StatusUsersLocations.objects.filter(user=request.user, status=1) | \
                     StatusUsersLocations.objects.filter(user=request.user, status=2)
    user_locations = [i.location.pk for i in user_locations_pre]
    # BY LOCATION
    # eligible_events_date_locations = {}
    # for i in user_locations:
    #     events = events_list(date_from=None, date_to=None, location=i)
    #     eligible_events_date_locations[i] = events

    # BY DATES
    eligible_events_date_locations = events_list(date_from=None, date_to=None, location=user_locations)

    if request.user.user_type == 3:
        location_manager = Location.objects.filter(manager_location=request.user).first()
        return render(request, 'index.html', context={"events": eligible_events_date_locations,
                                                      "location": location_manager, "date_to":date_to})
    return render(request, 'index.html', context={"events": eligible_events_date_locations, "date_to":date_to})


@login_required(login_url='/login/')
def all_users_site(request):
    status_users_location = StatusUsersLocations.objects.filter(status=1) | StatusUsersLocations.objects.filter(status=2)
    return render(request, 'benevoles.html', context={"status_users_location": status_users_location})


@login_required(login_url='/login/')
def users_site(request, location_id):
    if request.user.user_type == 2:
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
                return redirect(reverse('users_site', kwargs={'location_id': location_id}))
        return render(request, 'benevoles_site.html', context={"status_users_location": status_users_location, "form": form})


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
                return redirect(reverse('users_site', kwargs={'location_id': location_id}))


@login_required(login_url='/login/')
def profile(request):
    date_to = get_date_to()
    user_locations_pre = StatusUsersLocations.objects.filter(user=request.user, status=1) | StatusUsersLocations.objects.filter(user=request.user, status=2)
    user_locations = [i.location for i in user_locations_pre]
    return render(request, 'profile.html', context={'locations': user_locations, "date_to":date_to})
