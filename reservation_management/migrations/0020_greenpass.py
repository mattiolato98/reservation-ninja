# Generated by Django 3.2.7 on 2021-10-22 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation_management', '0019_alter_reservation_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='GreenPass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drive_link', models.URLField(default=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='green_pass', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
