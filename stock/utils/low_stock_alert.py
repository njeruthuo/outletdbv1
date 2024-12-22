from notification.models import Notification, NotificationChoices


def notify_admin_low_stock(sender=None, receiver=None, shop=None, product=None):
    if not receiver:
        print("Error: Receiver is None")
        return  # Avoid proceeding with invalid data

    try:
        notification = Notification.objects.create(
            sender=sender,
            receiver=receiver,
            shop=shop,
            notification_type=NotificationChoices.STOCKDEPLETED,
        )
        # notification.product_remaining.add(product)
        # notification.save()
        print("Notification created successfully")
    except Exception as e:
        print(f"An error occurred while creating notification: {e}")
