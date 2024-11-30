from django.urls import path,re_path

from ext_apis.consumers import TransactionConsumer

from .import views

urlpatterns = [
    path("initiate-payment/", views.mpesa_api_view, name="initiate_payment"),
    path("callback/", views.payment_callback, name="payment_callback"),
    # re_path(
    #     r'ws/transaction/(?P<receipt_id>[\w-]+)/$', TransactionConsumer.as_asgi()),
]
