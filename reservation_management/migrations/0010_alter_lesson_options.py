# Generated by Django 3.2.7 on 2021-10-17 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_management', '0009_remove_lesson_start_before_end'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['day', 'start_time']},
        ),
    ]
