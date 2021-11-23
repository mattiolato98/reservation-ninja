from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class PlatformUser(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    is_manager = models.BooleanField(default=False)

    unimore_username = models.CharField(max_length=500)
    unimore_password = models.CharField(max_length=500)
    credentials_ok = models.BooleanField(default=True)

    enable_automatic_reservation = models.BooleanField(default=True)
    feedback = models.BooleanField(default=True)
    ask_for_feedback = models.BooleanField(default=True)

    whats_new = models.BooleanField(default=True)
    instagram = models.BooleanField(default=True)

    privacy_and_cookie_policy_acceptance = models.BooleanField(default=False)

    green_pass_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username

    def get_day_lessons(self, day_idx, exclude=False, lesson_id=None ):
        if not exclude:
            return self.lessons.filter(day=day_idx)
        else:
            return self.lessons.filter(day=day_idx).exclude(id=lesson_id)

    @property
    def today_lessons(self):
        return self.lessons.filter(day=datetime.today().weekday())

    @property
    def lessons_count(self):
        return len(self.lessons.all())

    @property
    def plain_unimore_username(self):
        decryptor = Fernet(settings.CRYPTOGRAPHY_KEY.encode())
        return decryptor.decrypt(self.unimore_username.encode()).decode()

    @property
    def plain_unimore_password(self):
        decryptor = Fernet(settings.CRYPTOGRAPHY_KEY.encode())
        return decryptor.decrypt(self.unimore_password.encode()).decode()
