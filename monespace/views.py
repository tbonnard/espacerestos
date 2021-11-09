from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .models import Location, StatusUsersLocations, User
from .views_events import events_list
from .forms import StatusUsersLocationsForm


@login_required(login_url='/login/')
def index(request):
    #user_locations = Location.objects.filter(users=request.user)
    user_locations_pre = StatusUsersLocations.objects.filter(user=request.user, status=1) | \
                     StatusUsersLocations.objects.filter(user=request.user, status=2)
    user_locations = [i.location.pk for i in user_locations_pre]
    print(user_locations)
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
                                                      "location": location_manager})
    return render(request, 'index.html', context={"events": eligible_events_date_locations})


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
        return render(request, 'benevoles.html', context={"status_users_location": status_users_location, "form": form})


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
    user_locations = Location.objects.filter(users=request.user)
    return render(request, 'profile.html', context={'locations': user_locations})
