from django.urls import re_path

from ext_apis.consumers import MpesaTransactionConsumer

websocket_urlpatterns = [
    re_path(
        r'ws/transaction/(?P<receipt_id>[\w-]+)/$', MpesaTransactionConsumer.as_asgi()),
]
