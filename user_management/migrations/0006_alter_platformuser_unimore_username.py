# Generated by Django 3.2.7 on 2021-10-14 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0005_alter_platformuser_unimore_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformuser',
            name='unimore_username',
            field=models.CharField(max_length=500),
        ),
    ]
