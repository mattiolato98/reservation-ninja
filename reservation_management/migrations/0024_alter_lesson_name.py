# Generated by Django 3.2.7 on 2021-11-22 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_management', '0023_auto_20211122_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]