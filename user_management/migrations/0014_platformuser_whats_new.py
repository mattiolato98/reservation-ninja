# Generated by Django 3.2.7 on 2021-10-24 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0013_platformuser_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformuser',
            name='whats_new',
            field=models.BooleanField(default=True),
        ),
    ]
