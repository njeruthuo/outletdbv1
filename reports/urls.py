from django.urls import path

from . import views


urlpatterns = [
    path('report_api_view/', views.report_api_view, name='report_api_view')
]
