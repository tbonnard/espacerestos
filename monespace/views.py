from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .models import Location, StatusUsersLocations, LogsStatusUsersLocations, User, AttendeesEvents
from .views_events import events_list
from .forms import StatusUsersLocationsForm, UserProfileForm
from .functions_global import get_date_to, forbidden_to_user, admin_only


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


@admin_only
@login_required(login_url='/login/')
def all_users_site(request):
    users = User.objects.all()
    form = StatusUsersLocationsForm()
    status_users_location = StatusUsersLocations.objects.filter(status=1) | StatusUsersLocations.objects.filter(status=2)
    return render(request, 'benevoles.html', context={"status_users_location": status_users_location, "form": form, "users":users})


@forbidden_to_user
@login_required(login_url='/login/')
def users_site(request, location_id):
    if request.user.user_type == 3 and Location.objects.get(pk=location_id) not in Location.objects.filter(manager_location=request.user):
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


@forbidden_to_user
@login_required(login_url='/login/')
def user_site_update_status(request, location_id):
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


@login_required(login_url='/login/')
def profile_edit(request):
    form = UserProfileForm(instance=request.user)
    if request.method == "POST":
        form = UserProfileForm(data=request.POST)
        if form.is_valid():
            updated_user = request.user
            try:
                image = request.FILES['profile_picture']
            except:
                pass
            else:
                updated_user.profile_picture.save(image.name, image)
            finally:
                updated_user.first_name = form.cleaned_data['first_name']
                updated_user.last_name = form.cleaned_data['last_name']
                updated_user.address = form.cleaned_data['address']
                updated_user.city = form.cleaned_data['city']
                updated_user.zip_code = form.cleaned_data['zip_code']
                updated_user.tel = form.cleaned_data['tel']
                updated_user.save()
                return redirect('profile')
    return render(request, 'profile_edit.html', context={"form" : form})
