from . import views
from django.urls import path

urlpatterns = [
    path('stock_api_view/', views.stock_api_view, name='stock_api_view'),
]
