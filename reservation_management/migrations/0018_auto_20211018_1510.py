# Generated by Django 3.2.7 on 2021-10-18 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_management', '0017_alter_building_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
