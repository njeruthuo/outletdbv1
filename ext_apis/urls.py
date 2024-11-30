from django.urls import path

from .import views

urlpatterns = [
    path("initiate-payment/", views.mpesa_api_view, name="initiate_payment"),
    path("callback/", views.payment_callback, name="payment_callback"),
    
]
