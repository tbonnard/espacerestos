import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Event, Location, Message, User, StatusUsersLocations, AttendeesEvents, MessageSeen


@login_required(login_url='/login/')
def send_message(request):
    data = json.loads(request.body)
    date = data.get('date')
    all_site = data.get('all_site')
    group = data.get('group')
    description = data.get('description')
    user_uuid = data.get('user')
    try:
        users_to = User.objects.get(uuid=user_uuid)
    except:
        users_to = None

    event_uuid = data.get('event')
    try:
        event = Event.objects.get(uuid=event_uuid)
    except:
        event = None
    site_uuid = data.get('site')
    try:
        location = Location.objects.get(uuid=site_uuid)
    except:
        location = None

    new_message = Message(to_event=event, to_location=location, from_user=request.user, to_event_group=group,
                          description=description, info_all_locations=all_site, to_event_date=date, to_user=users_to)
    new_message.save()

    # send message

    return JsonResponse({"Success": "Le message a été envoyé"}, status=200)


def get_to_user_messages(user):
    to_user_events_pre = StatusUsersLocations.objects.filter(user=user, status=2)
    all_to_user_events = [i.distrib for i in to_user_events_pre]
    messages_events = Message.objects.filter(to_event__in=all_to_user_events)
    all_attend_to_user_events = []
    attend_to_user_events = []
    non_attend_to_user_events = []
    to_user_events_groups = []
    for i in messages_events:
        if i.to_event_group == 1:
            all_attend_to_user_events.append(i)
            to_user_events_groups.append(i.id)
        elif i.to_event_group == 2:
            if AttendeesEvents.objects.filter(user=user, parent_event=i.to_event, event_date=i.to_event_date):
                attend_to_user_events.append(i)
                to_user_events_groups.append(i.id)
        elif i.to_event_group == 3:
            if not AttendeesEvents.objects.filter(user=user, parent_event=i.to_event, event_date=i.to_event_date):
                non_attend_to_user_events.append(i)
                to_user_events_groups.append(i.id)
    to_user_distrib = []
    for i in messages_events:
        if i.to_event_group is None:
            to_user_distrib.append(i)
    to_user_locations_pre = StatusUsersLocations.objects.filter(user=user, status=2)
    to_user_locations = [i.location for i in to_user_locations_pre]
    to_user_messages = Message.objects.filter(to_user=user) | Message.objects.filter(id__in=to_user_events_groups) \
                       | Message.objects.filter(to_location__in=to_user_locations) \
                       | Message.objects.filter(info_all_locations=True )
    to_user_messages_tuple = tuple(to_user_messages.order_by('-created'))
    return to_user_messages_tuple


def get_from_user_messages(user):
    from_user_messages = Message.objects.filter(from_user=user)
    return from_user_messages.order_by('-created')


@login_required(login_url='/login/')
def get_info_if_new_messages(request):
    messages = get_to_user_messages(request.user)
    messages_seen = [i.message for i in MessageSeen.objects.filter(user=user)]
    new_message = []
    for i in messages:
        if i not in messages_seen:
            new_message.append(i)
    return JsonResponse([i.serialize() for i in new_message], safe=False)


def get_messages_seen(user):
    messages = get_to_user_messages(user)
    messages_seen = [i.message for i in MessageSeen.objects.filter(user=user)]
    new_message = []
    for i in messages:
        if i not in messages_seen:
            new_message.append(i)
    return new_message


@login_required(login_url='/login/')
def create_messages_seen(request):
    if request.method == 'POST':
        user = request.user
        messages = get_messages_seen(user)
        for i in messages:
            if not MessageSeen.objects.filter(user=user, message=i):
                new_seen = MessageSeen(user=user, message=i)
                new_seen.save()
        return JsonResponse(True, safe=False)
