from django.urls import path
from . import views

urlpatterns = [
    path('shop_api_view/', views.shop_api_view, name='shop_api_view'),
    path('shop_disbursement/', views.shop_stock_mgt_api, name='shop_disbursement'),
    path('complete-purchase-calculations/',
         views.shop_stock_mgt_api, name='shop_disbursement'),
    path('shop_stock_disbursement_api_view/',
         views.shop_stock_disbursement_api_view, name='shop_stock_disbursement_api_view'),
]
