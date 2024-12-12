from notification.middleware import get_current_request
from notification.models import Notification, NotificationChoices
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Stock


@receiver(post_save, sender=Stock)
def stock_reorder_level_crossed_pre_save(sender, instance, *args, **kwargs):
    """Check if the stock levels fall below reorder level and notify"""
    request = get_current_request()
    if not request:
        return

    instance.refresh_from_db()

    if instance.quantity <= instance.reorder_level:
        Notification.objects.create(
            sender=request.user,
            receiver=request.user,
            notification_type=NotificationChoices.STOCKDEPLETED
        )
