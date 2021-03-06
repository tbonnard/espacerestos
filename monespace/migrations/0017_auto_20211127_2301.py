# Generated by Django 3.2.9 on 2021-11-27 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0016_remove_event_was_recurring'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, choices=[('FR', 'France')], default='FR', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
        migrations.AddField(
            model_name='user',
            name='tel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='zip_code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.CharField(choices=[('FR', 'France')], default='FR', max_length=2),
        ),
    ]
