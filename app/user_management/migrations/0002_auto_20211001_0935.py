# Generated by Django 3.2.7 on 2021-10-01 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformuser',
            name='unimore_password',
            field=models.CharField(default='a', max_length=100),
        ),
        migrations.AddField(
            model_name='platformuser',
            name='unimore_username',
            field=models.CharField(default='a', max_length=100),
        ),
    ]