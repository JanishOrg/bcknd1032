# Generated by Django 4.0 on 2024-01-31 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_customusers_is_accepted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customusers',
            old_name='loaction_address',
            new_name='location_address',
        ),
        migrations.RenameField(
            model_name='pdlocation',
            old_name='drop_latitude',
            new_name='current_latitude',
        ),
        migrations.RenameField(
            model_name='pdlocation',
            old_name='drop_address',
            new_name='destination_address',
        ),
        migrations.RenameField(
            model_name='pdlocation',
            old_name='drop_longitude',
            new_name='destination_longitude',
        ),
        migrations.RemoveField(
            model_name='customusers',
            name='is_accepted',
        ),
        migrations.RemoveField(
            model_name='customusers',
            name='people_count',
        ),
        migrations.RemoveField(
            model_name='customusers',
            name='pickup_time',
        ),
        migrations.RemoveField(
            model_name='pdlocation',
            name='pickup_address',
        ),
        migrations.RemoveField(
            model_name='pdlocation',
            name='pickup_latitude',
        ),
        migrations.RemoveField(
            model_name='pdlocation',
            name='pickup_longitude',
        ),
        migrations.AddField(
            model_name='pdlocation',
            name='people_count',
            field=models.IntegerField(default=int),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pdlocation',
            name='pickup_time',
            field=models.CharField(default=int, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pdlocation',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
