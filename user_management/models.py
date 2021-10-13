from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class PlatformUser(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    is_manager = models.BooleanField(default=False)

    unimore_username = models.CharField(max_length=100)
    unimore_password = models.CharField(max_length=100)

    enable_automatic_reservation = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        encryptor = Fernet(settings.CRYPTOGRAPHY_KEY.encode())
        self.unimore_password = encryptor.encrypt(self.unimore_password.encode()).decode()
        super(PlatformUser, self).save(*args, **kwargs)

    @property
    def today_lessons(self):
        return self.lessons.filter(day=datetime.today().weekday())

    @property
    def clear_unimore_password(self):
        decryptor = Fernet(settings.CRYPTOGRAPHY_KEY.encode())
        return decryptor.decrypt(self.unimore_password.encode()).decode()
