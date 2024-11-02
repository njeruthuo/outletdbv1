from django.db import models
from django.contrib.auth.models import AbstractUser

from shop.models import Shop


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
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="operators", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)
