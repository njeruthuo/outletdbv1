from django.contrib.auth import get_user_model
from django.db import models

from stock.models import Stock

User = get_user_model()


class NotificationChoices(models.TextChoices):
    """Choices for Notifications"""
    STOCKDEPLETED = 'STOCK DEPLETED', 'STOCK DEPLETED'
    STOCKDISBURSED = 'STOCK DISBURSED', 'STOCK DISBURSED'


class NotificationStatuses(models.TextChoices):
    """Statuses for notification"""
    READ = 'READ', 'READ'
    UNREAD = 'UNREAD', 'UNREAD'


class Notification(models.Model):
    """User notifications to request/receive disbursements"""
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_notifications'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_notifications'
    )
    notification_type = models.CharField(choices=NotificationChoices.choices, max_length=300,
                                         default=NotificationChoices.STOCKDEPLETED)
    notification_status = models.CharField(
        max_length=200, choices=NotificationStatuses.choices, default=NotificationStatuses.UNREAD)
    product_remaining = models.ManyToManyField(Stock)

    def __str__(self):
        return f"{self.sender.email} notifies {self.receiver.email}"
