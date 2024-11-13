from django.contrib import admin
from .models import *


class ShopStockAdmin(admin.TabularInline):
    list_display = ['get_product_name']
    model = ShopStock
    extra = 1

    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = "Product Name"


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    inlines = [ShopStockAdmin]
    list_display = ['branch_name', 'location',
                    'opening_date', 'weight_tat', 'avg_weekly_profit', 'licenses','coordinates']

    search_fields = ['branch_name', 'location']
