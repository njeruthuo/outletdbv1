from django.db import models


class Shop(models.Model):
    branch_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    # decide whether one shop could have multiple operators
    # you can place this in users file to allow more users to a shop
    # operators = models.ForeignKey()
    weight_tat = models.PositiveIntegerField()
    profit_per_day = models.DecimalField(decimal_places=2, max_digits=10)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Outlet distribution center {self.branch_name} - {self.location}"
