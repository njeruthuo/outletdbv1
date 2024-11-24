from .models import *
from users.models import User

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price_per_item', 'reorder_level']


class ShopStockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ShopStock
        fields = ['id', 'product', 'quantity']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'photo', 'phone_number']


class ShopSerializer(serializers.ModelSerializer):
    stock = ShopStockSerializer(
        source='shop_stocks', many=True, required=False)
    operators = UserSerializer(many=True, required=False)

    class Meta:
        model = Shop
        fields = ['stock', 'branch_name',
                  'location', 'opening_date', 'weight_tat', 'avg_weekly_profit', 'licenses', 'coordinates', 'operators']
