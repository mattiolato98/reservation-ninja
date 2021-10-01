from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

from reservation_management.models import Lesson


class PlatformUser(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    is_manager = models.BooleanField(default=False)

    unimore_username = models.CharField(max_length=100)
    unimore_password = models.CharField(max_length=100)

    enable_automatic_reservation = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def today_lessons(self):
        return Lesson.objects.filter(day=datetime.today().weekday())
