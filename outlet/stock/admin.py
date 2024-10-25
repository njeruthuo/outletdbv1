from django.contrib import admin

# Register your models here.
from .models import Stock, Product, Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_item', 'category', 'brand']
