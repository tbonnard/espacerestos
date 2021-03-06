# Generated by Django 3.2.9 on 2021-12-16 03:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0038_auto_20211215_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='statususerslocations',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default='2021-12-16'),
        ),
    ]
