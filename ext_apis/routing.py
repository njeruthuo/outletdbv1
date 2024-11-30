from django.urls import path,re_path
from .consumers import TransactionConsumer

websocket_urlpatterns = [
    re_path(r'ws/transaction/$', TransactionConsumer.as_asgi()),
]
