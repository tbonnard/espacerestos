# Generated by Django 3.2.9 on 2021-12-19 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0039_auto_20211216_0352'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_managers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events_manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default='2021-12-19'),
        ),
    ]
