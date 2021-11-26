# Generated by Django 3.2.9 on 2021-11-15 19:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0010_attendeesevents_plus_other'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendeesevents',
            name='event_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='attendeesevents',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]