from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .models import Location, User, StatusUsersLocations
from .forms import LocationForm, SelectLocationsForm
from .notification_manager import send_email


def edit_user_type_to_manager(user):
    if user.user_type !=1:
        user.user_type = 3
        user.save()


def edit_user_type_to_user(user):
    """
    Edit user that is currently manager to another user type ("user")
    If user have multi-sites, he remains manager
    :param user: user for which we want to update status
    :return:
    """
    user_manager_other_location = Location.objects.filter(manager_location=user)
    if user_manager_other_location.count() ==1:
        user.user_type = 2
        user.save()


def check_if_new_status_to_create_update(location, user_to_update, manager):
    """
    Check if the status-location of the user must be updated depending on:
    - user is/becomes a manager
    - user is a user and asks to be part of the location
    - user already has other status (rejected, declined, ...)
    :param location: location object for which the status might be updated
    :param user_to_update: user object for which the status might be updated
    :param manager: boolean: if true, status of the user is active directly while if False, it is 'pending'
    :return: return status updated or None if no status updated
    """
    final_user_status = None
    if StatusUsersLocations.objects.filter(location=location, user=user_to_update).exclude(status=3).exclude(status=4).exclude(status=5):
        if StatusUsersLocations.objects.filter(location=location, user=user_to_update, status=1).first():
            if manager or location.manager_location == user_to_update:
                status_to_update = StatusUsersLocations.objects.filter(location=location, user=user_to_update, status=1).first()
                status_to_update.status = 2
                status_to_update.save()
                final_user_status = status_to_update
        else:
            if manager or location.manager_location == user_to_update:
                new_status = StatusUsersLocations(location=location, user=user_to_update, status=2)
                final_user_status = new_status
            else:
                new_status = StatusUsersLocations(location=location, user=user_to_update)
                final_user_status = new_status
    else:
        if manager or location.manager_location == user_to_update:
            new_status = StatusUsersLocations(location=location, user=user_to_update, status=2)
        else:
            new_status = StatusUsersLocations(location=location, user=user_to_update)
        new_status.save()
        final_user_status = new_status
    return final_user_status


@login_required(login_url='/login/')
def location_create(request):
    if request.user.user_type != 1:
        return redirect('index')
    else:
        form = LocationForm()
        if request.method == "POST":
            form = LocationForm(data=request.POST)
            if form.is_valid():
                new_location = form.save()
                edit_user_type_to_manager(new_location.manager_location)
                check_if_new_status_to_create_update(new_location, new_location.manager_location, True)
                return redirect('index')
        return render(request, 'location.html', context={"form": form})


@login_required(login_url='/login/')
def location_edit(request, location_id):
    if request.user.user_type == 2:
        return redirect('index')
    else:
        location_page = Location.objects.get(id=location_id)
        form = LocationForm(instance=location_page)
        if request.method == "POST":
            form = LocationForm(data=request.POST)
            if form.is_valid():
                location_page.name = form.cleaned_data['name']
                location_page.address_number = form.cleaned_data['address_number']
                location_page.address = form.cleaned_data['address']
                location_page.address_2 = form.cleaned_data['address_2']
                location_page.city = form.cleaned_data['city']
                location_page.zip_code = form.cleaned_data['zip_code']
                location_page.country = form.cleaned_data['country']
                try:
                    manager = User.objects.get(id=request.POST['manager_location'])
                except User.DoesNotExist:
                    location_page.manager_location = None
                else:
                    if location_page.manager_location != manager:
                        edit_user_type_to_user(location_page.manager_location)
                        location_page.manager_location = manager
                        edit_user_type_to_manager(manager)
                        check_if_new_status_to_create_update(location_page, manager, True)
                location_page.save()
                return redirect('index')
        return render(request, 'location.html', context={"form": form, 'is_edit': True, 'location_id': location_id})


@login_required(login_url='/login/')
def location_details(request, location_id):
    location_page = Location.objects.get(id=location_id)
    if location_page:
        return render(request, 'location_details.html', context={"location": location_page})
    return redirect('index')


@login_required(login_url='/login/')
def locations(request):
    if request.user.user_type == 1:
        all_locations = Location.objects.all()
        return render(request, 'locations.html', context={"all_locations": all_locations, "admin":True })
    elif Location.objects.filter(manager_location=request.user).count() == 1:
        return redirect(reverse('location_details', kwargs={'location_id': Location.objects.filter(manager_location=request.user).first().pk}))
    elif request.user.user_type == 3:
        all_locations = Location.objects.filter(manager_location=request.user)
        return render(request, 'locations.html', context={"all_locations": all_locations})
    else:
        return redirect('index')


@login_required(login_url='/login/')
def select_locations(request):
    try:
        status_user_locations = StatusUsersLocations.objects.filter(user=request.user, status=1) | StatusUsersLocations.objects.filter(user=request.user, status=2)
        locations_user_status = [i.location.pk for i in status_user_locations]
    except:
        form = SelectLocationsForm()
    else:
        form = SelectLocationsForm(initial={'locations':locations_user_status})
    if request.method == "POST":
        form = SelectLocationsForm(data=request.POST)
        if form.is_valid():
            locations_form = form.cleaned_data['locations']
            print(locations_form)
            for i in locations_form:
                status_check = check_if_new_status_to_create_update(i, request.user, False)
                if status_check is not None and status_check.status == 1:
                    try:
                        send_email(request.user, i.manager_location.email)
                    except:
                        print('error - email send notif status location manager')
            print(StatusUsersLocations.objects.filter(user=request.user).exclude(status=3).exclude(status=4).exclude(status=5))
            for j in StatusUsersLocations.objects.filter(user=request.user).exclude(status=3).exclude(status=4).exclude(status=5):
                print(j.location)
                if (j.location not in locations_form and request.user.user_type !=1) and (j.location not in locations_form and j.location.manager_location != request.user):
                    j.status =5
                    j.save()
        return redirect('index')
    return render(request, 'select_locations.html', context={"form": form})