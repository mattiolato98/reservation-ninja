# Generated by Django 3.2.7 on 2021-11-10 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0016_rename_ask_feedback_platformuser_ask_for_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformuser',
            name='instagram',
            field=models.BooleanField(default=True),
        ),
    ]
