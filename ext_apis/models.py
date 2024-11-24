from typing import Iterable
from django.db import models

from shop.models import Shop
from stock.models import Product
from users.models import User

# Create your models here.


class TransactionTypeChoices(models.TextChoices):
    CASH = 'CASH SALE', 'CASH SALE'
    CASHLESS = 'M-PESA', 'M-PESA'


class TransactionStatusChoices(models.TextChoices):
    COMPLETED = 'COMPLETE', 'COMPLETE'
    PENDING = 'PENDING', 'PENDING'


class TransactionLog(models.Model):
    mpesa_transaction_code = models.CharField(
        max_length=50, primary_key=False, unique=True, null=True)
    transaction_type = models.CharField(
        max_length=25, choices=TransactionTypeChoices.choices, default=TransactionTypeChoices.CASHLESS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    # auto calculate the profit here
    profit = models.DecimalField(max_digits=20, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    customer_number = models.CharField(max_length=50)
    receipt_ID = models.CharField(
        max_length=200, primary_key=False, unique=True)
    transaction_status = models.CharField(
        choices=TransactionStatusChoices.choices, max_length=15)

    """Here, we will perform calculations for profit and save"""

    def __str__(self) -> str:
        return f"{self.transaction_type} sale by {self.user.username} from {self.shop.branch_name} is {self.transaction_status}"

    class Meta:
        indexes = [
            models.Index(fields=['date_created']),
            models.Index(fields=['mpesa_transaction_code', 'date_created']),
            models.Index(fields=['date_created',
                                 'customer_number', 'receipt_ID', 'transaction_status']),
            models.Index(fields=['mpesa_transaction_code', 'date_created', 'user',
                                 'customer_number', 'receipt_ID', 'transaction_type', 'transaction_status']),
        ]
