from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from .models import Event, AttendeesEvents, RecurringPattern


@login_required(login_url='/login/')
def api_get_all_attendees_user(request):
    attendees = AttendeesEvents.objects.filter(user=request.user)
    return JsonResponse([i.serialize() for i in attendees], safe=False)


@login_required(login_url='/login/')
def api_attend_decline_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        attendee_type = data.get('type')
        event = Event.objects.get(pk=data.get('parent_event'))
        date = data.get('event_date')
        if event.is_recurring:
            rec_pattern = RecurringPattern.objects.filter(event=event).first()
        else:
            rec_pattern = None
        if attendee_type == "attend":
            new_attendee = AttendeesEvents(user=request.user, parent_event=event, event_date=date,
                                           recurring_pattern=rec_pattern, time_from=event.time_from, time_to=event.time_to)
            new_attendee.save()
            return JsonResponse({"message": 'OK'}, status=201)
        elif attendee_type == "decline":
            attend_decline = AttendeesEvents.objects.filter(user=request.user, parent_event=event, event_date=date)
            attend_decline.delete()
            return JsonResponse({"message": 'OK'}, status=201)
        elif attendee_type == "plus_other":
            attend_to_update = AttendeesEvents.objects.filter(user=request.user, parent_event=event, event_date=date).first()
            attend_to_update.plus_other = data.get('plus_other')
            attend_to_update.save()
            return JsonResponse({"message": 'OK'}, status=201)
        else:
            return JsonResponse({"error": "try again - not a POST"}, status=400)
    return JsonResponse({"error": "try again - not a POST"}, status=400)


@login_required(login_url='/login/')
def api_get_specific_attendees(request):
    event = Event.objects.get(pk=request.GET['parent_event'])
    date = request.GET['event_date']
    attendees = AttendeesEvents.objects.filter(user=request.user, parent_event=event, event_date=date)
    return JsonResponse([i.serialize() for i in attendees], safe=False)



