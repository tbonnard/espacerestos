# Generated by Django 3.2.9 on 2021-12-20 01:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0041_auto_20211219_2257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_manager',
        ),
        migrations.AddField(
            model_name='messageseen',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default='2021-12-20'),
        ),
    ]