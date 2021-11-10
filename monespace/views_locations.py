from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Location, User, StatusUsersLocations
from .forms import LocationForm, SelectLocationsForm
from .notification_manager import send_email


def edit_user_type_to_manager(user):
    user.user_type = 3
    user.save()


def edit_user_type_to_user(user):
    user_manager_other_location = Location.objects.filter(manager_location=user)
    if user_manager_other_location.count() ==1:
        user.user_type = 2
        user.save()


def check_if_new_status_to_create_update(location, manager):
    try:
        status_to_update = StatusUsersLocations.objects.filter(location=location, user=manager)
    except:
        new_status = StatusUsersLocations(location=location, user=manager, status=2)
        new_status.save()
    else:
        status_check = []
        for i in status_to_update:
            status_check.append(i.status)
        if 1 in status_check and 2 in status_check:
            status_to_delete = StatusUsersLocations.objects.filter(location=location, user=manager, status=1).first()
            status_to_delete.delete()
        elif 1 in status_check:
            status_to_update = StatusUsersLocations.objects.filter(location=location, user=manager, status=1).first()
            status_to_update.status = 2
            status_to_update.save()
        elif 2 in status_check:
            pass
        else:
            new_status = StatusUsersLocations(location=location, user=manager, status=2)
            new_status.save()


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
                check_if_new_status_to_create_update(new_location, new_location.manager_location)
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
                        check_if_new_status_to_create_update(location_page, manager)
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
    if request.user.user_type != 1:
        return redirect('index')
    else:
        all_locations = Location.objects.all()
        return render(request, 'locations.html', context={"all_locations": all_locations})


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
            for i in form.cleaned_data['locations']:
                i.users.add(request.user)
                if not StatusUsersLocations.objects.filter(location=i, user=request.user, status=1) \
                        or not not StatusUsersLocations.objects.filter(location=i, user=request.user, status=2):
                    new_status = StatusUsersLocations(location=i, user=request.user)
                    new_status.save()
                    try:
                        send_email(request.user, i.manager_location.email)
                    except:
                        print('error - email send notif status location manager')
            for j in StatusUsersLocations.objects.filter(user=request.user):
                if j.location not in form.cleaned_data['locations']:
                    j.location.users.remove(request.user)
                    j.status = 5
                    j.save()
        return redirect('index')
    return render(request, 'select_locations.html', context={"form": form})
