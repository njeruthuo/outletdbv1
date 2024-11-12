from django.urls import path


from . import views

urlpatterns = [
    path('login/', views.user_api_view, name='user-api'),
    path('register_new_employees/', views.user_api_view, name='user-api'),
]
