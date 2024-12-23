from .import views

from django.urls import path, re_path

from ext_apis.consumers import TransactionConsumer


urlpatterns = [
    path("initiate-payment/", views.mpesa_api_view, name="initiate_payment"),
    path("callback/", views.payment_callback, name="payment_callback"),

    path('transaction_logs_api_view/', views.transaction_logs_api_view,
         name='transaction_logs_api_view'),
    # re_path(
    #     r'ws/transaction/(?P<receipt_id>[\w-]+)/$', TransactionConsumer.as_asgi()),
]
