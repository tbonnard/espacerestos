# Generated by Django 3.2.9 on 2021-11-04 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0013_auto_20211104_1955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='recurring_pattern',
        ),
        migrations.AddField(
            model_name='recurringpattern',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='monespace.event'),
            preserve_default=False,
        ),
    ]
