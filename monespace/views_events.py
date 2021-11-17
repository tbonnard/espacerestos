from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime

from .models import Event, Location, RecurringPattern, StatusUsersLocations, AttendeesEvents, \
    EventExceptionCancelledRescheduled
from .forms import EventForm, EventRecurringPatternForm
from .functions_global import get_date_to


def events_list(date_from, date_to, location, date_cancelled=None):
    """
    Get all events based on parameters
    :param date_from:
    :param date_to:
    :param location:
    :return: List of events - objects
    """
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
        # all_events = Event.objects.filter(location=location)
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
                        if not EventExceptionCancelledRescheduled.objects.filter(is_cancelled=True, parent_event=j, start_date=event_date):
                            try:
                                events = eligible_events_date[event_date]
                                events.append(j)
                                eligible_events_date[event_date] = events
                            except KeyError:
                                eligible_events_date.setdefault(event_date, [j])
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
        date_to = get_date_to()
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
        if request.user.user_type == 1:
            user_locations = Location.objects.all()
        eligible_events_date = events_list(date_from, date_to, user_locations)

        attendees = AttendeesEvents.objects.filter(user=request.user)

    return render(request, 'all_events.html',
                  context={"events": eligible_events_date, "date_to": date_to.strftime("%Y-%m-%d"),
                           "attendees": attendees})


def create_event_unit(form):
    try:
        Location.objects.get(id=form['location'].value())
    except:
        location = None
    else:
        location = Location.objects.get(id=form['location'].value())
    finally:
        new_event = Event(name=form.cleaned_data['name'].title(),
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
        form = EventForm()
        if request.user.user_type == 1:
            form.fields['location'].queryset = Location.objects.all()
            if Location.objects.all().count() == 1:
                form.initial["location"] = Location.objects.all().first()
        else:
            form.fields['location'].queryset = Location.objects.all().filter(manager_location=request.user)
            if Location.objects.all().filter(manager_location=request.user).count() == 1:
                form.initial["location"] = Location.objects.all().filter(manager_location=request.user).first()
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


def validate_event_date(event, date):
    event_valid = False
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[-2:])
    date_in_datetime = datetime.datetime(year, month, day)
    date_in_date = datetime.date(year, month, day)
    if event.is_recurring:
        eligible_event_date = events_list(date_in_datetime, date_in_datetime, None)
        for i in eligible_event_date:
            for j in i[1]:
                if i[0] == date_in_date and j == event:
                    event_valid = True
    else:
        if event.start_date == date_in_date:
            event_valid = True
    return event_valid


@login_required(login_url='/login/')
def event_details(request, event_id):
    try:
        date = request.GET['date']
        event_page = Event.objects.get(id=event_id)
    except:
        return redirect('index')
    else:
        if validate_event_date(event_page, date):
            attendees = AttendeesEvents.objects.filter(user=request.user, parent_event=Event.objects.get(pk=event_id),
                                                       event_date=date).first()
            all_attendees = AttendeesEvents.objects.filter(parent_event=Event.objects.get(pk=event_id), event_date=date)
            count_attendees = all_attendees.count()
            for i in all_attendees:
                count_attendees += i.plus_other
            if event_page.location.manager_location == request.user:
                manager_location = True
            else:
                manager_location = False
            if event_page:
                return render(request, 'event_details.html',
                              context={"event": event_page, "manager_location": manager_location, 'date': date,
                                       "attendees": attendees, "all_attendees": all_attendees,
                                       "count_attendees": count_attendees})
        return redirect('index')


@login_required(login_url='/login/')
def event_delete_all(request, event_id):
    if request.user.user_type == 2:
        return redirect('index')
    else:
        try:
            event_to_delete = Event.objects.get(id=event_id)
        except:
            return redirect('index')
        else:
            rec_pattern = RecurringPattern.objects.filter(event=event_to_delete).first()
            event_date = event_to_delete.start_date
            new_number_occurences=0
            for n in range(rec_pattern.max_num_occurrences + 1):
                if datetime.datetime(event_to_delete.start_date.year, event_to_delete.start_date.month, event_to_delete.start_date.day) <= datetime.datetime(event_date.year, event_date.month, event_date.day) <= datetime.datetime.now():
                    if not EventExceptionCancelledRescheduled.objects.filter(is_cancelled=True, parent_event=event_to_delete,
                                                                             start_date=event_date):
                        new_number_occurences +=1
                    else:
                        break
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
            if new_number_occurences == 0:
                event_to_delete.delete()
            else:
                rec_pattern.max_num_occurrences = new_number_occurences -1
                rec_pattern.save()
            return redirect('index')


@login_required(login_url='/login/')
def event_delete_rec(request, event_id):
    if request.user.user_type == 2:
        return redirect('index')
    try:
        date = request.GET['date']
        event_rec_to_delete = Event.objects.get(id=event_id)
    except:
        return redirect('index')
    else:
        rec_to_delete_exception = EventExceptionCancelledRescheduled(
            location=event_rec_to_delete.location,
            name=event_rec_to_delete.name,
            description=event_rec_to_delete.description,
            start_date=date,
            end_date=event_rec_to_delete.end_date,
            time_from=event_rec_to_delete.time_from,
            time_to=event_rec_to_delete.time_to,
            is_cancelled=True,
            is_rescheduled=False,
            is_full_day=event_rec_to_delete.is_full_day,
            parent_event=event_rec_to_delete,
        )
        rec_to_delete_exception.save()
        for i in AttendeesEvents.objects.filter(parent_event=event_rec_to_delete, event_date=date):
            i.delete()
        return redirect('index')
