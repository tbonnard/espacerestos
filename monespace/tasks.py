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
    # print(list_users)
    send_email(5, list_users, email_gmail, date=date_to)


@shared_task()
def say_hello():
    print('bonjour')