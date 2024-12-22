from rest_framework import serializers

from .models import Notification, models

from shop.serializers import ShopStockSerializer


class NotificationSerializer(serializers.ModelSerializer):
    sender_shop = serializers.SerializerMethodField()
    shop_stocks_below_reorder = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'notification_status',
                  'notification_type', 'sender_shop', 'shop_stocks_below_reorder']

    def get_sender_shop(self, obj):
        shop = obj.sender.operated_shop.first()
        return shop.branch_name if shop else None

    def get_shop_stocks_below_reorder(self, obj):
        if obj.shop is None:
            return []
        shop_stocks = obj.shop.shop_stocks.filter(
            quantity__lte=models.F('reorder_level'))
        return ShopStockSerializer(shop_stocks, many=True).data
