from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .forms import EventForm, EventRecurringPatternForm, DistributionForm
from .functions_global import forbidden_to_user
from .models import Location, Event, RecurringPattern
from .views_events import default_initial_event_form, create_event_unit, create_recurring_pattern_event_unit


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
            new_rec = RecurringPattern(event=new_event, separation_count=1, max_num_occurrences=104, repeat_each_x=0)
            new_rec.save()
            return redirect('index')
    return render(request, 'distrib_create.html', context={"form": form, "location": location})

