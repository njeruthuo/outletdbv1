from rest_framework import serializers

from ext_apis.models import TransactionLog
from users.models import User
from shop.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['branch_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class TransactionLogSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()
    user = UserSerializer()

    class Meta:
        model = TransactionLog
        fields = ['customer_number', 'date_created', 'id', 'mpesa_transaction_code',
                  'product_quantities',
                  'products',
                  'profit',
                  'receipt_ID',
                  'shop',
                  'transaction_status',
                  'transaction_type',
                  'user']
