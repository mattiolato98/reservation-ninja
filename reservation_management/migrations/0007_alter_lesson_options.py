# Generated by Django 3.2.7 on 2021-10-17 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_management', '0006_reservation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['day']},
        ),
    ]
