# Generated by Django 3.2.7 on 2021-10-01 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0003_auto_20211001_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformuser',
            name='enable_automatic_reservation',
            field=models.BooleanField(default=False),
        ),
    ]
