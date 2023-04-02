from django.db import models

from django.contrib.auth.models import AbstractUser


class AppUser(AbstractUser):
    phone_number = models.CharField(max_length=255)
    birth_date = models.CharField(max_length=255, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
