# Generated by Django 3.2.9 on 2021-12-06 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0024_remove_location_manager_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
