# Generated by Django 3.2.7 on 2021-11-06 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0015_platformuser_ask_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platformuser',
            old_name='ask_feedback',
            new_name='ask_for_feedback',
        ),
    ]