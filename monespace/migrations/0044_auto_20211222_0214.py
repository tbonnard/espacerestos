# Generated by Django 3.2.9 on 2021-12-22 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0043_remove_user_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='message',
            name='to_event_manger_group',
            field=models.IntegerField(blank=True, choices=[(1, 'Aux responsables de la distribution'), (2, 'A tous les bénévoles et responsables')], null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default='2021-12-22'),
        ),
    ]
