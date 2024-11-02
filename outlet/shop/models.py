from django.db import models

from stock.models import Stock


class Shop(models.Model):
    branch_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    opening_date = models.DateTimeField(auto_now_add=True)
    weight_tat = models.PositiveIntegerField(default=0)
    avg_weekly_profit = models.DecimalField(
        decimal_places=2, max_digits=10, blank=True, null=True, default=0)
    licenses = models.FileField(upload_to='licenses')
    current_load = models.ManyToManyField(
        Stock, blank=True)

    def __str__(self):
        return f"Outlet distribution center {self.branch_name} - {self.location}"
