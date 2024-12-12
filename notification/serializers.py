from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    sender_shop = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id','notification_status',
                  'notification_type', 'sender_shop']

    def get_sender_shop(self, obj):
        shop = obj.sender.operated_shop.first()
        return shop.branch_name if shop else None
