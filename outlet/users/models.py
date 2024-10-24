from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


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

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)
