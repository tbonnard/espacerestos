from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Location
from .views_events import events_list


@login_required(login_url='/login/')
def index(request):
    user_locations = Location.objects.filter(users=request.user)

    #BY LOCATION
    eligible_events_date_locations = {}
    for i in user_locations:
        events = events_list(date_from=None, date_to=None, location=i)
        eligible_events_date_locations[i] = events

    # BY DATES

    if request.user.user_type == 3:
        location_manager = Location.objects.filter(manager_location=request.user).first()
        return render(request, 'index.html', context={"events": eligible_events_date_locations,
                                                      "location":location_manager})
    return render(request, 'index.html', context={"events": eligible_events_date_locations})


@login_required(login_url='/login/')
def users_site(request, location_id):
    if request.user.user_type == 2:
        return redirect('index')
    else:
        locations_users = Location.objects.get(pk=location_id).users.all()
        return render(request, 'benevoles.html', context={"users": locations_users})


@login_required(login_url='/login/')
def profile(request):
    user_locations = Location.objects.filter(users=request.user)
    return render(request, 'profile.html', context={'locations':user_locations})

