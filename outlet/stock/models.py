from django.db import models


class CategoryChoices(models.TextChoices):
    DRYFOODS = 'DRYFOODS', 'DRYFOODS'
    TOILETRIES = 'TOILETRIES', 'TOILETRIES'


# class Category(models.Model):
#     class Meta:
#         verbose_name_plural = 'Categories'

#         indexes = [
#             models.Index(fields=['name'])
#         ]


#     def __str__(self) -> str:
#         return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    reorder_level = models.PositiveIntegerField(default=10)
    price_per_item = models.DecimalField(decimal_places=2, max_digits=12)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=50, choices=CategoryChoices.choices, default=CategoryChoices.DRYFOODS)

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
        return f"{self.product.name} - {self.quantity} units"
