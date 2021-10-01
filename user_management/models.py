from django.contrib.auth.models import AbstractUser
from django.db import models


class PlatformUser(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    is_manager = models.BooleanField(default=False)

    unimore_username = models.CharField(max_length=100)
    unimore_password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
