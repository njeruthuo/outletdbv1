from django.contrib import admin

# Register your models here.
from .models import Stock, Product, Brand, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'contact']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['get_product_name', 'quantity', 'last_updated']

    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Product Name'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_item', 'category', 'brand']
    search_fields = ('name', 'brand','category')
