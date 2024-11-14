from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.phone_number_formatter import phone_number_formatter


class TextChoices(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    MANAGER = 'Manager', 'Manager'
    EMPLOYEE = 'Employee', 'Employee'


class User(AbstractUser):
    access_level = models.CharField(
        max_length=20,
        choices=TextChoices.choices,
        default=TextChoices.EMPLOYEE,
    )

    phone_number = models.CharField(max_length=25, null=True, blank=True)
    photo = models.ImageField(upload_to='profile', blank=True)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email

        if self.phone_number:
            print(self.phone_number)
            self.phone_number = phone_number_formatter(self.phone_number)

        super(User, self).save(*args, **kwargs)
