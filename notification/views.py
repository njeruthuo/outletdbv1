from django.db.transaction import atomic

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import NotificationSerializer

from notification.models import Notification, NotificationStatuses
from users.authentication import TokenAuthentication


class NotificationsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    """Handles notifications"""

    def get(self, request, *args, **kwargs):
        """extracts the user from request & checking if they have notifications"""
        if not request.user.is_authenticated:
            return Response({"ERROR": "AUTHENTICATION REQUIRED."}, status=status.HTTP_401_UNAUTHORIZED)

        notifications = Notification.objects.filter(
            receiver=request.user).order_by('-id')
        serializer = NotificationSerializer(notifications, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @atomic
    def post(self, request, *args, **kwargs):
        id = request.data

        try:
            notification = Notification.objects.get(id=id)
        except Notification.DoesNotExist:
            return Response({'FAILED': 'COULD NOT FIND THE NOTIFICATION'}, status=status.HTTP_404_NOT_FOUND)

        notification.notification_status = NotificationStatuses.READ
        notification.save()

        return Response({'SUCCESS': 'NOTIFICATION MARKED READ'}, status=status.HTTP_200_OK)


notification_api_view = NotificationsAPI.as_view()
