from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from notification.middleware import get_current_request
from notification.models import Notification, NotificationChoices


class Brand(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name'])
        ]


class Product(models.Model):
    name = models.CharField(max_length=100)
    reorder_level = models.PositiveIntegerField(default=10)
    price_per_item = models.DecimalField(decimal_places=2, max_digits=12)
    product_buying_price = models.DecimalField(
        decimal_places=2, max_digits=12, default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name', 'category', 'brand'])
        ]

    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stock_items")
    reorder_level = models.PositiveIntegerField(default=10)
    quantity = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} restocked"


@receiver(pre_save, sender=Stock, dispatch_uid="stock_reorder_signal", weak=False)
def stock_reorder_level_crossed_pre_save(sender, instance, *args, **kwargs):
    request = get_current_request()
    if not request:
        return

    instance.refresh_from_db()

    print(instance.quantity)

    if instance.quantity < instance.reorder_level:
        notification = Notification.objects.create(
            sender=request.user,
            receiver=request.user,
            notification_type=NotificationChoices.STOCKDEPLETED
        )
