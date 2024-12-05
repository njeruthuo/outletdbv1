from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class NotificationChoices(models.TextChoices):
    STOCKDEPLETED = 'STOCK DEPLETED', 'STOCK DEPLETED'
    STOCKDISBURSED = 'STOCK DISBURSED', 'STOCK DISBURSED'


class Notification(models.Model):
    sender = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sent_notification')
    receiver = models.OneToOneField(User, on_delete=models.CASCADE, related_name='received_notification')
    notification_type = models.CharField(choices=NotificationChoices.choices, max_length=300,
                                         default=NotificationChoices.STOCKDEPLETED)

    def __str__(self):
        return f"{self.sender.email} notifies {self.receiver.email}"
