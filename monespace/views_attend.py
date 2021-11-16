from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Event, AttendeesEvents


@login_required(login_url='/login/')
def api_get_all_attendees_user(request):
    attendees = AttendeesEvents.objects.filter(user=request.user)
    return JsonResponse([i.serialize() for i in attendees], safe=False)


@login_required(login_url='/login/')
def api_attend_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        event = Event.objects.get(pk=data.get('parent_event'))
        date = data.get('event_date')
        new_attendee = AttendeesEvents(user=request.user, parent_event=event, event_date=date)
        new_attendee.save()
        return JsonResponse({"message": 'OK'}, status=201)
    return JsonResponse({"error": "try again - not a POST"}, status=400)


@login_required(login_url='/login/')
def api_decline_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        event = Event.objects.get(pk=data.get('parent_event'))
        date = data.get('event_date')
        attend_decline = AttendeesEvents.objects.filter(user=request.user, parent_event=event, event_date=date)
        attend_decline.delete()
        return JsonResponse({"message": 'OK'}, status=201)
    return JsonResponse({"error": "try again - not a POST"}, status=400)







# OLD
# .replace(',', '').replace('.', ''), '%b %d %Y'
@login_required(login_url='/login/')
def api_get_attendees(request):
    event = Event.objects.get(pk=request.GET['parent_event'])
    date = datetime.strptime(request.GET['event_date'])
    attendees = AttendeesEvents.objects.filter(user=request.user, parent_event=event, event_date=date)
    return JsonResponse([i.serialize() for i in attendees], safe=False)


@login_required(login_url='/login/')
def attend_event(request):
    if request.method == "POST":
        try:
            event = Event.objects.get(pk=request.POST['parent_event'])
            date = request.POST['event_date']
        except:
            return redirect('index')
        else:
            try:
                plus_other = int(request.POST['plus_other'])
            except:
                new_attendee = AttendeesEvents(user=request.user, parent_event=event, event_date=date)
            else:
                new_attendee = AttendeesEvents(user=request.user, parent_event=event, event_date=date, plus_other=plus_other)
            finally:
                new_attendee.save()
        return redirect('index')
    return redirect('index')


@login_required(login_url='/login/')
def decline_event(request):
    if request.method == "POST":
        try:
            event = Event.objects.get(pk=request.POST['parent_event'])
            date = request.POST['event_date']
        except:
            return redirect('index')
        else:
            attend_decline = AttendeesEvents.objects.filter(user=request.user, parent_event=event, event_date=date)
            attend_decline.delete()
        return redirect('index')
    return redirect('index')