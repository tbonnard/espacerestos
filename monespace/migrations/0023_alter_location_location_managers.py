# Generated by Django 3.2.9 on 2021-12-03 21:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0022_alter_location_location_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_managers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]