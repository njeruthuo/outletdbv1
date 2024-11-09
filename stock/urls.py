from . import views
from django.urls import path

urlpatterns = [
    # Stock URLS
    path('stock_api_view/', views.stock_api_view, name='stock_api_view'),
    path('stock_api_view/<int:pk>/', views.stock_api_view, name='stock_api_view'),

    # Categories URLS
    path('category_api_view/', views.category_api_view, name='category_api_view'),
    path('category_api_view/<int:pk>/',
         views.category_api_view, name='category_api_view'),

    # Brand serializer
    path('brand_api_view/', views.brand_api_view, name='brand_api_view'),
    path('brand_api_view/<int:pk>/',
         views.brand_api_view, name='brand_api_view'),
]
