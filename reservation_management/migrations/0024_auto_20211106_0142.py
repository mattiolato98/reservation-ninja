# Generated by Django 3.2.7 on 2021-11-06 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_management', '0023_alter_feedback_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='user',
        ),
        migrations.DeleteModel(
            name='Log',
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]
