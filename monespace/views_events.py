from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
import pprint

from .models import Event, Location, RecurringPattern, StatusUsersLocations
from .forms import EventForm, EventRecurringPatternForm


def events_list(date_from, date_to, location):
    if date_from is None:
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    else:
        date_from = date_from - datetime.timedelta(days=1)

    if date_to is None:
        days = 14
        days_added = datetime.timedelta(days=days)
        date_to = date_from + days_added
    else:
        date_to = date_to

    if location is not None:
        #all_events = Event.objects.filter(location=location)
        all_events = [Event.objects.filter(location=i) for i in location]
    else:
        all_events = [Event.objects.all()]

    eligible_events_date = {}
    for i in range(len(all_events)):
        for j in all_events[i]:
            event_date = j.start_date
            if j.is_recurring:
                rec_pattern = RecurringPattern.objects.filter(event=j).first()
                for n in range(rec_pattern.max_num_occurrences + 1):
                    if date_from <= datetime.datetime(event_date.year, event_date.month, event_date.day) <= date_to:
                        try:
                            # events = eligible_events_date[event_date]['events']
                            events = eligible_events_date[event_date]
                            events.append(j)
                            eligible_events_date[event_date] = events
                        except KeyError:
                            eligible_events_date.setdefault(event_date, [j])
                            # eligible_events_date.setdefault(event_date, {'events':[all_events[0][i]]})
                    if rec_pattern.repeat_each_x == 0:
                        event_date = event_date + datetime.timedelta(days=rec_pattern.separation_count * 7)
                    elif rec_pattern.repeat_each_x == 1:
                        event_date = event_date + datetime.timedelta(days=rec_pattern.separation_count * 1)
                    elif rec_pattern.repeat_each_x == 2:
                        event_date = event_date + datetime.timedelta(weeks=rec_pattern.separation_count * 4)
                    elif rec_pattern.repeat_each_x == 3:
                        event_date = event_date + datetime.timedelta(weeks=rec_pattern.separation_count * 12)
                    elif rec_pattern.repeat_each_x == 4:
                        event_date = event_date + datetime.timedelta(weeks=rec_pattern.separation_count * 24)
                    elif rec_pattern.repeat_each_x == 5:
                        event_date = event_date + datetime.timedelta(weeks=rec_pattern.separation_count * 56)
            else:
                if date_from <= datetime.datetime(event_date.year, event_date.month, event_date.day) <= date_to:
                    try:
                        events = eligible_events_date[event_date]
                        events.append(j)
                        eligible_events_date[event_date] = events
                    except KeyError:
                        eligible_events_date.setdefault(event_date, [j])
    sorted_eligible_events_date = sorted(eligible_events_date.items())
    return sorted_eligible_events_date


@login_required(login_url='/login/')
def events_list_date(request):
    try:
        request.GET['from']
        date_from = datetime.datetime.strptime(request.GET['from'], '%Y-%m-%d')
    except:
        date_from = None
    try:
        request.GET['to']
        date_to = datetime.datetime.strptime(request.GET['to'], '%Y-%m-%d')
    except:
        date_to = None
    try:
        request.GET['location']
        location = [Location.objects.get(pk=request.GET['location'])]
    except:
        user_locations_pre = StatusUsersLocations.objects.filter(user=request.user, status=1) | \
                         StatusUsersLocations.objects.filter(user=request.user, status=2)
        user_locations = [i.location.pk for i in user_locations_pre]
    else:
        user_locations = [i.pk for i in location]
    finally:
        eligible_events_date = events_list(date_from, date_to, user_locations)
    return render(request, 'all_events.html', context={"events": eligible_events_date})


def create_event_unit(form):
    try:
        Location.objects.get(id=form['location'].value())
    except:
        location = None
    else:
        location = Location.objects.get(id=form['location'].value())
    finally:
        new_event = Event(name=form.cleaned_data['name'],
                          description=form.cleaned_data['description'],
                          start_date=form.cleaned_data['start_date'],
                          time_from=form.cleaned_data['time_from'],
                          time_to=form.cleaned_data['time_to'],
                          is_recurring=form.cleaned_data['is_recurring'],
                          is_full_day=form.cleaned_data['is_full_day'],
                          location=location
                          )
        new_event.save()
        return new_event


def edit_event_unit(event, form):
    """
    Need the object of the event, not the ID
    :param: event: object to edit, form: form valid
    :return: return the event object
    """
    event.name = form.cleaned_data['name']
    event.description = form.cleaned_data['description']
    event.start_date = form.cleaned_data['start_date']
    event.end_date = form.cleaned_data['end_date']
    event.time_from = form.cleaned_data['time_from']
    event.time_to = form.cleaned_data['time_to']
    event.is_recurring = form.cleaned_data['is_recurring']
    event.is_full_day = form.cleaned_data['is_full_day']
    try:
        Location.objects.get(id=form['location'].value())
    except:
        event.location = None
    else:
        event.location = Location.objects.get(id=form['location'].value())
    finally:
        event.save()
        return event


def create_recurring_pattern_event_unit(event, form):
    new_recurring = RecurringPattern(event=event,
                                     separation_count=form.cleaned_data['separation_count'],
                                     max_num_occurrences=form.cleaned_data['max_num_occurrences'],
                                     # day_of_week=form.cleaned_data['day_of_week'],
                                     # week_of_month=form.cleaned_data['week_of_month'],
                                     # day_of_month=form.cleaned_data['day_of_month'],
                                     # month_of_year=form.cleaned_data['month_of_year'],
                                     repeat_each_x=form.cleaned_data['repeat_each_x']
                                     )
    new_recurring.save()
    return new_recurring


def edit_recurring_pattern_event_unit(recurring_pattern, form):
    """
    Need the object of the recurring pattern, not the ID
    :param: recurring_pattern: object to edit, form: form valid
    :return: the object recurring_pattern
    """
    recurring_pattern.separation_count = form.cleaned_data['separation_count']
    recurring_pattern.max_num_occurrences = form.cleaned_data['max_num_occurrences']
    # recurring_pattern.day_of_week = form.cleaned_data['day_of_week']
    # recurring_pattern.week_of_month = form.cleaned_data['week_of_month']
    # recurring_pattern.day_of_month = form.cleaned_data['day_of_month']
    # recurring_pattern.month_of_year = form.cleaned_data['month_of_year']
    recurring_pattern.repeat_each_x = form.cleaned_data['repeat_each_x']
    recurring_pattern.save()
    return recurring_pattern


@login_required(login_url='/login/')
def event_create(request):
    if request.user.user_type == 2:
        return redirect('index')
    else:
        form = EventForm(initial={"location":Location.objects.filter(manager_location=request.user).first()})
        rec_form = EventRecurringPatternForm()
        if request.method == "POST":
            form = EventForm(data=request.POST)
            rec_form = EventRecurringPatternForm(data=request.POST)
            if form.is_valid() and rec_form.is_valid():
                new_event = create_event_unit(form)
                if new_event.is_recurring:
                    create_recurring_pattern_event_unit(event=new_event, form=rec_form)
                return redirect('index')
        return render(request, 'event.html', context={"form": form, "rec_form": rec_form})


@login_required(login_url='/login/')
def event_edit(request, event_id):
    if request.user.user_type == 2:
        return redirect('index')
    else:
        event_page = Event.objects.get(id=event_id)
        form = EventForm(instance=event_page)
        if event_page.is_recurring:
            event_rec_pattern = RecurringPattern.objects.filter(event=event_page).first()
            rec_form = EventRecurringPatternForm(instance=event_rec_pattern)
        else:
            rec_form = EventRecurringPatternForm()
        if request.method == "POST":
            form = EventForm(data=request.POST)
            rec_form = EventRecurringPatternForm(data=request.POST)
            if form.is_valid() and rec_form.is_valid():
                edit_event_unit(event=event_page, form=form)
                if event_page.is_recurring:
                    if RecurringPattern.objects.filter(event=event_page).first():
                        edit_recurring_pattern_event_unit(
                            recurring_pattern=RecurringPattern.objects.filter(event=event_page).first(),
                            form=rec_form)
                    else:
                        create_recurring_pattern_event_unit(event=event_page, form=rec_form)
                else:
                    if RecurringPattern.objects.filter(event=event_page).first():
                        RecurringPattern.objects.filter(event=event_page).first().delete()
                return redirect('index')
        return render(request, 'event.html',
                      context={"form": form, "rec_form": rec_form, 'is_edit': True, 'event_id': event_id})


@login_required(login_url='/login/')
def event_details(request, event_id):
    event_page = Event.objects.get(id=event_id)
    if event_page.location.manager_location == request.user:
        manager_location = True
    else:
        manager_location = False
    if event_page:
        return render(request, 'event_details.html', context={"event": event_page, "manager_location":manager_location})
    return redirect('index')
