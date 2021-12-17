import os
from celery import Celery
from datetime import timedelta
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'espacerestos.settings')
app = Celery('espacerestos')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "every_day": {
        "task": "monespace.tasks.send_2_days_reminder",
        "schedule": crontab(day_of_week="0-6", hour=9, minute=00),
    },
}

app.autodiscover_tasks()
