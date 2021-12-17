import datetime
from celery import shared_task
import environ

from .models import Event, AttendeesEvents, User, RecurringPattern, EventExceptionCancelledRescheduled
from .views_events import events_list, return_date_based_pattern
from .notification_manager import send_email


env = environ.Env()
# reading .env file
environ.Env.read_env()
email_gmail = env("email_gmail")


@shared_task()
def send_2_days_reminder():
    print('bonjour')
    today = datetime.datetime.now()
    days = 2
    days_added = datetime.timedelta(days=days)
    date_to = today + days_added
    # print(date_to.strftime("%Y-%m-%d"))
    attendees = AttendeesEvents.objects.filter(event_date=date_to.strftime("%Y-%m-%d"))
    list_users = []
    for y in attendees:
        # print(y.event_date)
        list_users.append(y.user)

    # all_events = Event.objects.all()
    # list_users = []
    # for i in all_events:
    #     event_date = i.start_date
    #     if i.is_recurring:
    #         rec_pattern = RecurringPattern.objects.filter(event=i).first()
    #         for n in range(rec_pattern.max_num_occurrences + 1):
    #             if datetime.datetime(event_date.year, event_date.month, event_date.day).strftime("%Y-%m-%d") == date_to.strftime("%Y-%m-%d"):
    #                 if not EventExceptionCancelledRescheduled.objects.filter(is_cancelled=True, parent_event=i, start_date=event_date):
    #                     attendees = AttendeesEvents.objects.filter(parent_event=i, event_date=event_date)
    #                     for y in attendees:
    #                         list_users.append(y.user)
    #             event_date = return_date_based_pattern(rec_pattern, event_date)
    # print(list_users)
    #send_email(5, list_users, email_gmail)

