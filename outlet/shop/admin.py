from django.contrib import admin
from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['branch_name', 'location',
                    'opening_date', 'weight_tat', 'avg_weekly_profit', 'licenses']

    search_fields = ['branch_name', 'location']
