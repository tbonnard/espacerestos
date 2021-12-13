from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
import datetime

from .models import Location, StatusUsersLocations, LogsStatusUsersLocations, User, AttendeesEvents, Event
from .views_events import events_list
from .forms import StatusUsersLocationsForm, UserProfileForm
from .functions_global import get_date_to, forbidden_to_user, admin_only


@login_required(login_url='/login/')
def index(request):
    # if request.user.user_type == 1:
    #     user_locations = Location.objects.all()
    # else:
    user_distrib_pre = StatusUsersLocations.objects.filter(user=request.user, status=1) | \
                         StatusUsersLocations.objects.filter(user=request.user, status=2)
    distrib_user_choice = [i.distrib for i in user_distrib_pre if not i.distrib.is_cancelled]
    distrib_attendees = [i.parent_event for i in AttendeesEvents.objects.filter(user=request.user)]
    distrib = [i for i in distrib_user_choice]
    for i in distrib_attendees:
        if i not in distrib and not i.is_cancelled:
            distrib.append(i)
    eligible_events_date_locations = events_list(date_from=None, date_to=None, location=None, distrib=distrib, event_manager=None)

    pending_location = []
    if StatusUsersLocations.objects.filter(user=request.user, status=1):
        # pending_location = [i.location for i in StatusUsersLocations.objects.filter(user=request.user, status=1)]
        pending_events = StatusUsersLocations.objects.filter(user=request.user, status=1)
    else:
        pending_events = None

    eligible_events_date_locations_attendees = []
    attendees = AttendeesEvents.objects.filter(user=request.user)
    for i in eligible_events_date_locations:
        for j in i[1]:
            for z in attendees:
                if j['uuid'] == z.parent_event.uuid and i[0] == z.event_date:
                    for y in eligible_events_date_locations_attendees:
                        if y[0] == i[0]:
                            for x in eligible_events_date_locations_attendees:
                                if x[0] == i[0]:
                                    events_that_date_index = eligible_events_date_locations_attendees.index(x)
                                    break
                            events_that_date = eligible_events_date_locations_attendees[events_that_date_index][1]
                            events_that_date.append(j)
                            for a in eligible_events_date_locations_attendees:
                                if a[0] == i[0]:
                                    eligible_events_date_locations_attendees[eligible_events_date_locations_attendees.index(a)] = (i[0], events_that_date)
                                    break
                    if i[0] not in eligible_events_date_locations_attendees:
                        eligible_events_date_locations_attendees.append(i[0])
                    eligible_events_date_locations_attendees[eligible_events_date_locations_attendees.index(i[0])]=(i[0],[j])
    eligible_events_date_locations_attendees_final = []
    dates_event = []
    for b in eligible_events_date_locations_attendees:
        if b[0] not in dates_event:
            dates_event.append(b[0])
            eligible_events_date_locations_attendees_final.append(b)
    date_to = datetime.datetime.now() - datetime.timedelta(days=1) + datetime.timedelta(weeks=8)
    events_manager = events_list(date_from=None, date_to=date_to, location=None, event_manager=request.user, distrib=None)
    return render(request, 'index.html', context={"events": eligible_events_date_locations_attendees_final,
                                                  "date_to": date_to, "pending_events":pending_events,
                                                  "attendees": attendees, "events_manager": events_manager })


def faq_view(request):
    return render(request, 'faq.html')


@login_required(login_url='/login/')
@admin_only
def all_users_site(request):
    users = User.objects.all()
    form = StatusUsersLocationsForm()
    status_users_location = StatusUsersLocations.objects.filter(status=1) | StatusUsersLocations.objects.filter(status=2)
    return render(request, 'benevoles.html', context={"status_users_location": status_users_location, "form": form, "users":users})


@login_required(login_url='/login/')
@forbidden_to_user
def users_site(request, location_id):
    if request.user.user_type == 3 and Location.objects.get(uuid=location_id) not in Location.objects.filter(location_managers=request.user):
        return redirect('index')
    else:
        status_users_location = StatusUsersLocations.objects.filter(location=Location.objects.get(uuid=location_id),
                                                                    status=1) | StatusUsersLocations.objects.filter(
            location=Location.objects.get(uuid=location_id), status=2)
        users_pre = [i.user for i in status_users_location]
        users=[]
        for i in users_pre:
            if i not in users:
                users.append(i)

        form = StatusUsersLocationsForm()

        if request.method == "POST":
            try:
                user_status_update = StatusUsersLocations.objects.get(uuid=request.GET['id'])
            except:
                pass
            else:
                user_status_update.status = 2
                user_status_update.save()
                logs = LogsStatusUsersLocations(location=user_status_update.location, from_user=request.user, user=user_status_update.user, status=2, current_status=user_status_update.status)
                logs.save()
                return redirect(reverse('users_site', kwargs={'location_id': location_id}))
        return render(request, 'benevoles_site.html', context={'location_id': location_id, "status_users_location": status_users_location, "form": form, "users":users})


@login_required(login_url='/login/')
@forbidden_to_user
def user_site_update_status(request, location_id):
    if request.method == "POST":
        try:
            user_status_update = StatusUsersLocations.objects.get(uuid=request.GET['id'])
        except:
            pass
        else:
            user_status_update.status = request.POST['status']
            user_status_update.save()
            logs = LogsStatusUsersLocations(location=user_status_update.location, from_user=request.user, user=user_status_update.user, status=request.POST['status'], current_status=user_status_update.status)
            logs.save()
            return redirect(reverse('users_site', kwargs={'location_id': location_id}))
    return redirect('index')


@login_required(login_url='/login/')
def profile(request):
    date_to = get_date_to()
    user_distrib_pre = StatusUsersLocations.objects.filter(user=request.user, status=1) | StatusUsersLocations.objects.filter(user=request.user, status=2)
    user_distrib = [i for i in user_distrib_pre if not i.distrib.is_cancelled]
    # user_locations = [i.location for i in user_locations_pre]
    user_manager_locations = Location.objects.filter(location_managers=request.user)
    return render(request, 'profile.html', context={'distrib': user_distrib, "date_to":date_to,
                                                    'manager_locations': user_manager_locations})


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
                updated_user.email = form.cleaned_data['email']
                updated_user.address = form.cleaned_data['address']
                updated_user.city = form.cleaned_data['city']
                updated_user.zip_code = form.cleaned_data['zip_code']
                updated_user.tel = form.cleaned_data['tel']
                updated_user.save()
                return redirect('profile')
    return render(request, 'profile_edit.html', context={"form" : form})
