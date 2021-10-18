from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from datetime import datetime


class PlatformUser(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    is_manager = models.BooleanField(default=False)

    unimore_username = models.CharField(max_length=500)
    unimore_password = models.CharField(max_length=500)

    enable_automatic_reservation = models.BooleanField(default=True)

    privacy_and_cookie_policy_acceptance = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def clean(self):
        if self.email.split('@')[1] != 'studenti.unimore.it':
            raise ValidationError(_("Seems that you are not a Unimore student."))
        if not self.privacy_and_cookie_policy_acceptance:
            raise ValidationError(_("You must accept the privacy policies."))

        return super(PlatformUser, self).clean()

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
