# Generated by Django 3.2.9 on 2021-11-26 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0013_auto_20211126_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='was_recurring',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
