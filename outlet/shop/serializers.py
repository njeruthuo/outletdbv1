from .models import Shop

from rest_framework import serializers


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'branch_name', 'location',
                  'opening_date', 'weight_tat', 'avg_weekly_profit', 'licenses', 'current_load']
