from django.urls import path
from . import views

urlpatterns = [
    path('shop_api_view/', views.shop_api_view, name='shop_api_view'),
]
