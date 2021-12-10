from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import EventForm, EventRecurringPatternForm, DistributionForm, StatusUsersLocationsForm
from .functions_global import forbidden_to_user
from .models import Location, Event, RecurringPattern, StatusUsersLocations, LogsStatusUsersLocations
from .views_events import default_initial_event_form, create_event_unit, create_recurring_pattern_event_unit
from .views_locations import edit_user_type_to_manager, check_if_new_status_to_create_update


@forbidden_to_user
@login_required(login_url='/login/')
def distribution_create(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    form = DistributionForm()
    if request.method == "POST":
        form = DistributionForm(data=request.POST)
        if form.is_valid():
            new_event = Event(name=form.cleaned_data['name'], start_date=form.cleaned_data['start_date'],
                              end_date=form.cleaned_data['start_date'],
                              location=location, event_manager=form.cleaned_data['event_manager'],
                              time_from=form.cleaned_data['time_from'], time_to=form.cleaned_data['time_to'],
                              is_recurring=True, is_distrib=True)
            new_event.save()
            new_rec = RecurringPattern(event=new_event, separation_count=1, max_num_occurrences=999, repeat_each_x=0)
            new_rec.save()
            edit_user_type_to_manager(new_event.event_manager)
            check_if_new_status_to_create_update(distrib=new_event, location=new_event.location,
                                                 user_to_update=new_event.event_manager, from_user=request.user,
                                                 manager=True)
            return redirect('index')
    return render(request, 'distrib_create.html', context={"form": form, "location": location})


@forbidden_to_user
@login_required(login_url='/login/')
def distrib_details(request, distrib_id):
    distrib = get_object_or_404(Event, pk=distrib_id)
    if request.user.user_type == 3 and distrib.event_manager != request.user:
        return redirect('index')
    else:
        status_users_location = StatusUsersLocations.objects.filter(distrib=distrib, status=1) | \
                                StatusUsersLocations.objects.filter(distrib=distrib, status=2)
        form = StatusUsersLocationsForm()

        if request.method == "POST":
            try:
                user_status_update = StatusUsersLocations.objects.get(pk=request.GET['id'])
            except:
                pass
            else:
                user_status_update.status = 2
                user_status_update.save()
                logs = LogsStatusUsersLocations(distrib=distrib, location=user_status_update.location, from_user=request.user, user=user_status_update.user, status=2, current_status=user_status_update.status)
                logs.save()
                return redirect(reverse('distrib_details', kwargs={'distrib_id': distrib_id}))

    return render(request, 'distrib_details.html', context={"distrib":distrib,
                                                            "status_users_location": status_users_location,
                                                            "form": form})


@forbidden_to_user
@login_required(login_url='/login/')
def user_distrib_update_status(request, distrib_id):
    if request.method == "POST":
        try:
            user_status_update = StatusUsersLocations.objects.get(pk=request.GET['id'])
            distrib_user = get_object_or_404(Event, pk=distrib_id)
        except:
            pass
        else:
            user_status_update.status = request.POST['status']
            user_status_update.save()
            logs = LogsStatusUsersLocations(distrib=distrib_user, location=user_status_update.location, from_user=request.user, user=user_status_update.user, status=request.POST['status'], current_status=user_status_update.status)
            logs.save()
            return redirect(reverse('distrib_details', kwargs={'distrib_id': distrib_id}))
    return redirect('index')


