from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import DistributionForm, StatusUsersLocationsForm, DistributionManagerForm
from .functions_global import forbidden_to_user
from .models import Location, Event, RecurringPattern, StatusUsersLocations, LogsStatusUsersLocations, User
from .views_locations import edit_user_type_to_manager, check_if_new_status_to_create_update, edit_user_type_to_user


@login_required(login_url='/login/')
@forbidden_to_user
def distribution_create(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    form = DistributionForm()
    user_from_location = [i.pk for i in Location.objects.get(pk=location_id).location_managers.all()]
    form.fields['event_manager'].queryset = User.objects.filter(id__in=user_from_location)
    print(len(user_from_location))
    if len(user_from_location) == 1:
        form.initial['event_manager'] = User.objects.get(id=user_from_location[0])

    if request.method == "POST":
        form = DistributionForm(data=request.POST)
        if form.is_valid():
            new_event = Event(name=form.cleaned_data['name'], start_date=form.cleaned_data['start_date'],
                              end_date=form.cleaned_data['start_date'],
                              location=location, event_manager=form.cleaned_data['event_manager'],
                              time_from=form.cleaned_data['time_from'], time_to=form.cleaned_data['time_to'],
                              is_recurring=True, is_distrib=True)
            new_event.save()
            new_rec = RecurringPattern(event=new_event, separation_count=1, max_num_occurrences=260, repeat_each_x=0)
            new_rec.save()
            edit_user_type_to_manager(new_event.event_manager)
            check_if_new_status_to_create_update(distrib=new_event, location=new_event.location,
                                                 user_to_update=new_event.event_manager, from_user=request.user,
                                                 manager=True)
            return redirect('index')
    return render(request, 'distrib_create.html', context={"form": form, "location": location})


@forbidden_to_user
@login_required(login_url='/login/')
def distributions(request):
    # if request.user.user_type == 1:
    #     events = Event.objects.all()
    #     return render(request, 'distributions.html', context={"events": events})
    # if Event.objects.filter(event_manager=request.user).count() == 1:
    #     return redirect(reverse('distrib_details', kwargs={'distrib_id': Event.objects.filter(event_manager=request.user).first().pk}))
    # else:
    events = Event.objects.filter(event_manager=request.user)
    return render(request, 'distributions.html', context={"events": events})



@login_required(login_url='/login/')
@forbidden_to_user
def distrib_details(request, distrib_id):
    distrib = get_object_or_404(Event, pk=distrib_id)
    if distrib.is_cancelled:
        return redirect('index')
    if request.user.user_type == 3 and request.user not in distrib.location.location_managers.all():
        return redirect('index')
    else:
        status_users_location = StatusUsersLocations.objects.filter(distrib=distrib, status=1) | \
                                StatusUsersLocations.objects.filter(distrib=distrib, status=2)
        form = StatusUsersLocationsForm()
        user_from_location = [i.pk for i in Location.objects.get(pk=distrib.location.pk).location_managers.all()]
        formManager = DistributionManagerForm()
        formManager.fields['event_manager'].queryset = User.objects.filter(id__in=user_from_location)
        if len(user_from_location) ==1 :
            formManager.initial['event_manager'] = User.objects.get(id=user_from_location[0])

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
                                                            "form": form, "formManager":formManager})


@login_required(login_url='/login/')
@forbidden_to_user
def distrib_users(request, distrib_id):
    distrib = get_object_or_404(Event, pk=distrib_id)
    if request.user.user_type == 3 and request.user not in distrib.location.location_managers.all():
        return redirect('index')
    else:
        status_users_location = StatusUsersLocations.objects.filter(distrib=distrib, status=1) | \
                                StatusUsersLocations.objects.filter(distrib=distrib, status=2)
        form = StatusUsersLocationsForm()
        user_from_location = [i.pk for i in Location.objects.get(pk=distrib.location.pk).location_managers.all()]
        formManager = DistributionManagerForm()
        formManager.fields['event_manager'].queryset = User.objects.filter(id__in=user_from_location)
        if len(user_from_location) ==1 :
            formManager.initial['event_manager'] = User.objects.get(id=user_from_location[0])

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
            return redirect(reverse('distrib_users', kwargs={'distrib_id': distrib_id}))

    return render(request, 'benevoles_distrib.html', context={"distrib":distrib,
                                                            "status_users_location": status_users_location,
                                                            "form": form, "formManager":formManager})



@login_required(login_url='/login/')
@forbidden_to_user
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
            return redirect(reverse('distrib_users', kwargs={'distrib_id': distrib_id}))
    return redirect('index')


@login_required(login_url='/login/')
@forbidden_to_user
def change_distrib_manager(request, distrib_id):
    distrib = get_object_or_404(Event, pk=distrib_id)
    if request.user.user_type == 3 and request.user not in distrib.location.location_managers.all():
        return redirect('index')

    if request.method== "POST":
        distrib = get_object_or_404(Event, pk=distrib_id)
        distrib_manager = User.objects.get(pk=request.POST['event_manager'])
        previous_manager = distrib.event_manager
        distrib.event_manager = distrib_manager
        distrib.save()
        edit_user_type_to_manager(distrib.event_manager)
        edit_user_type_to_user(previous_manager)
        check_if_new_status_to_create_update(distrib=distrib, location=distrib.location,
                                             user_to_update=distrib.event_manager, from_user=request.user,
                                             manager=True)
        return redirect(reverse('distrib_details', kwargs={'distrib_id': distrib_id}))
    return redirect('index')


@login_required(login_url='/login/')
def get_event_location(request):
    all_event_distrib = Event.objects.filter(is_distrib=True, is_cancelled=False)
    return JsonResponse([i.serialize() for i in all_event_distrib], safe=False)


@login_required(login_url='/login/')
def get_user_distrib(request):
    status_user_distrib = StatusUsersLocations.objects.filter(user=request.user,
                                                                status=1) | StatusUsersLocations.objects.filter(
        user=request.user, status=2)
    return JsonResponse([i.serialize() for i in status_user_distrib], safe=False)


@login_required(login_url='/login/')
def get_count_event_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    event_loc_count = Event.objects.filter(is_distrib=True, is_cancelled=False, location=location).count()
    return JsonResponse(event_loc_count, safe=False)


@login_required(login_url='/login/')
@forbidden_to_user
def get_count_event_benev(request):
    status_user_distrib = StatusUsersLocations.objects.filter(status=1) | StatusUsersLocations.objects.filter(status=2)
    count_distrib_ben = {}
    for i in status_user_distrib:
        if i.distrib.pk in count_distrib_ben:
            if i.status == 1:
                count_distrib_ben[i.distrib.pk]['pending'] += 1
            else:
                count_distrib_ben[i.distrib.pk]['active'] += 1
        else:
            if i.status == 1:
                count_distrib_ben.setdefault(i.distrib.pk, {"pending":1, "active":0})
            else:
                count_distrib_ben.setdefault(i.distrib.pk, {"pending":0, "active":1})
    return JsonResponse(count_distrib_ben, safe=False)