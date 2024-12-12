"""Notifications urls"""

from django.urls import path
from .views import notification_api_view

urlpatterns = [
    path('notification_api_view/', notification_api_view, name='notification_api_view'),
]
