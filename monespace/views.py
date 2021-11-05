from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Event, Location, User, RecurringPattern
from .forms import EventForm, LocationForm, EventRecurringPatternForm


def index(request):
    all_events = Event.objects.all()
    all_locations = Location.objects.all()
    all_patterns = RecurringPattern.objects.all()
    return render(request, 'index.html', context={"events": all_events, 'locations': all_locations, 'patterns': all_patterns})


def create_event_unit(**kwargs):
    if Location.objects.get(id=kwargs['location']):
        location = Location.objects.get(id=kwargs['location'])
    else:
        location = None
    new_event = Event(name=kwargs['name'],
                      description=kwargs['description'],
                      start_date=kwargs['start_date'],
                      time_from=kwargs['time_from'],
                      time_to=kwargs['time_to'],
                      is_recurring=kwargs['is_recurring'],
                      is_full_day=kwargs['is_full_day'],
                      location=location
                      )
    new_event.save()
    return new_event


def edit_event_unit(**kwargs):
    """
    Need the object of the event, not the ID
    :param kwargs:
    :return: return the event object
    """
    event = kwargs['event']
    event.name = kwargs['name']
    event.description = kwargs['description']
    event.start_date = kwargs['start_date']
    event.end_date = kwargs['end_date']
    event.time_from = kwargs['time_from']
    event.time_to = kwargs['time_to']
    event.is_recurring = kwargs['is_recurring']
    event.is_full_day = kwargs['is_full_day']
    if Location.objects.get(id=kwargs['location']):
        event.location = Location.objects.get(id=kwargs['location'])
    else:
        event.location = None
    event.save()
    return event


def create_recurring_pattern_event_unit(**kwargs):
    new_recurring = RecurringPattern(event=kwargs['event'],
                                     separation_count=kwargs['separation_count'],
                                     max_num_occurrences=kwargs['max_num_occurrences'],
                                     day_of_week=kwargs['day_of_week'],
                                     # week_of_month=kwargs['week_of_month'],
                                     # day_of_month=kwargs['day_of_month'],
                                     # month_of_year=kwargs['month_of_year'],
                                     repeat_each_x = kwargs['repeat_each_x']
                                     )
    new_recurring.save()
    return new_recurring


def edit_recurring_pattern_event_unit(**kwargs):
    """
    Need the object of the recurring pattern, not the ID
    :param kwargs:
    :return: the object recurring_pattern
    """
    recurring_pattern = kwargs['recurring_pattern']
    recurring_pattern.separation_count = kwargs['separation_count']
    recurring_pattern.max_num_occurrences = kwargs['max_num_occurrences']
    recurring_pattern.day_of_week = kwargs['day_of_week']
    # recurring_pattern.week_of_month = kwargs['week_of_month']
    # recurring_pattern.day_of_month = kwargs['day_of_month']
    # recurring_pattern.month_of_year = kwargs['month_of_year']
    recurring_pattern.repeat_each_x = kwargs['repeat_each_x']
    recurring_pattern.save()
    return recurring_pattern


@login_required(login_url='/login/')
def event_create(request):
    form = EventForm()
    rec_form = EventRecurringPatternForm()
    if request.method == "POST":
        form = EventForm(data=request.POST)
        rec_form = EventRecurringPatternForm(data=request.POST)
        if form.is_valid() and rec_form.is_valid():
            new_event = create_event_unit(name=form.cleaned_data['name'],
                                          description=form.cleaned_data['description'],
                                          start_date=form.cleaned_data['start_date'],
                                          time_from=form.cleaned_data['time_from'],
                                          time_to=form.cleaned_data['time_to'],
                                          is_recurring=form.cleaned_data['is_recurring'],
                                          location=form['location'].value(),
                                          is_full_day=form.cleaned_data['is_full_day'],
                                          )
            if new_event.is_recurring:
                create_recurring_pattern_event_unit(event=new_event, separation_count=rec_form.cleaned_data['separation_count'],
                                                    max_num_occurrences=rec_form.cleaned_data['max_num_occurrences'],
                                                    day_of_week=rec_form.cleaned_data['day_of_week'],
                                                    # week_of_month=rec_form.cleaned_data[ 'week_of_month'],
                                                    # day_of_month=rec_form.cleaned_data['day_of_month'],
                                                    # month_of_year=rec_form.cleaned_data['month_of_year'],
                                                    repeat_each_x=rec_form.cleaned_data['repeat_each_x']
                                                    )
            return redirect('index')
    return render(request, 'event.html', context={"form": form, "rec_form": rec_form})


@login_required(login_url='/login/')
def event_edit(request, event_id):
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
            edit_event_unit(event=event_page, name=form.cleaned_data['name'],
                            description=form.cleaned_data['description'],
                            start_date=form.cleaned_data['start_date'], end_date=form.cleaned_data['end_date'],
                            time_from=form.cleaned_data['time_from'],
                            time_to=form.cleaned_data['time_to'], is_recurring=form.cleaned_data['is_recurring'],
                            location=form['location'].value(), is_full_day=form.cleaned_data['is_full_day'],
                            )
            if event_page.is_recurring:
                if RecurringPattern.objects.filter(event=event_page).first():
                   edit_recurring_pattern_event_unit(recurring_pattern=RecurringPattern.objects.filter(event=event_page).first(),
                                                    separation_count = rec_form.cleaned_data['separation_count'],
                                                     max_num_occurrences = rec_form.cleaned_data['max_num_occurrences'],
                                                     day_of_week = rec_form.cleaned_data['day_of_week'],
                                                     # week_of_month = rec_form.cleaned_data['week_of_month'],
                                                     # day_of_month = rec_form.cleaned_data['day_of_month'],
                                                     # month_of_year = rec_form.cleaned_data['month_of_year'],
                                                     repeat_each_x=rec_form.cleaned_data['repeat_each_x']
                                                     )
                else:
                    create_recurring_pattern_event_unit(event=event_page,
                                                        separation_count=rec_form.cleaned_data['separation_count'],
                                                        max_num_occurrences=rec_form.cleaned_data['max_num_occurrences'],
                                                        day_of_week=rec_form.cleaned_data['day_of_week'],
                                                        # week_of_month=rec_form.cleaned_data['week_of_month'],
                                                        # day_of_month=rec_form.cleaned_data['day_of_month'],
                                                        # month_of_year=rec_form.cleaned_data['month_of_year'],
                                                        repeat_each_x=rec_form.cleaned_data['repeat_each_x']
                                                        )
            else:
                if RecurringPattern.objects.filter(event=event_page).first():
                    RecurringPattern.objects.filter(event=event_page).first().delete()
            return redirect('index')
    return render(request, 'event.html',
                  context={"form": form, "rec_form": rec_form, 'is_edit': True, 'event_id': event_id})


@login_required(login_url='/login/')
def event_details(request, event_id):
    event_page = Event.objects.get(id=event_id)
    if event_page:
        return render(request, 'event_details.html', context={"event": event_page})
    return redirect('index')


@login_required(login_url='/login/')
def location_create(request):
    form = LocationForm()
    if request.method == "POST":
        form = LocationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'location.html', context={"form": form})


@login_required(login_url='/login/')
def location_edit(request, location_id):
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
                location_page.manager_location = User.objects.get(id=request.POST['manager_location'])
            except:
                location_page.manager_location = None
            location_page.save()
            return redirect('index')
    return render(request, 'location.html', context={"form": form, 'is_edit': True, 'location_id': location_id})


@login_required(login_url='/login/')
def location_details(request, location_id):
    location_page = Location.objects.get(id=location_id)
    if location_page:
        return render(request, 'location_details.html', context={"location": location_page})
    return redirect('index')


