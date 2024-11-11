from django.db import models
from stock.models import Product


# from django.contrib.gis.db import models as gis_models


class Shop(models.Model):
    branch_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    opening_date = models.DateTimeField(auto_now_add=True)
    weight_tat = models.PositiveIntegerField(default=0)
    avg_weekly_profit = models.DecimalField(
        decimal_places=2, max_digits=10, blank=True, null=True, default=0
    )
    licenses = models.FileField(upload_to="licenses")
    # coordinates = gis_models.PointField(
    #     geography=True, blank=True, null=True, default="POINT(0 0)")

    def __str__(self):
        return f"Outlet distribution center {self.branch_name} - {self.location}"


class ShopStock(models.Model):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name='shop_stocks')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='shop_products')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('shop', 'product')

    def __str__(self):
        return f"{self.shop.branch_name} - {self.product.name}: {self.quantity} units"


class StockDisbursement(models.Model):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name='disbursements')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='disbursements')
    disburse_quantity = models.PositiveIntegerField()
    # Optionally track the user or admin
    disbursed_by = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Disbursed {self.disburse_quantity} units of {self.product.name} "
                f"to {self.shop.branch_name} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
