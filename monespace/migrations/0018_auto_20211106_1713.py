# Generated by Django 3.2.9 on 2021-11-06 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0017_recurringpattern_repeat_each_x'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurringpattern',
            name='day_of_week',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='EventExceptionCancelledRescheduled',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('time_from', models.TimeField(blank=True, default='00:00:00')),
                ('time_to', models.TimeField(blank=True, default='00:00:00')),
                ('is_cancelled', models.BooleanField(default=False)),
                ('is_rescheduled', models.BooleanField(default=False)),
                ('is_full_day', models.BooleanField(default=False)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events_exceptions_locations', to='monespace.location')),
                ('parent_event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='monespace.event')),
            ],
        ),
        migrations.CreateModel(
            name='AttendeesEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('parent_event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='monespace.event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
