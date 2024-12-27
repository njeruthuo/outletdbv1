from django.urls import path


from . import views

urlpatterns = [
    path('login/', views.user_api_view, name='user-api'),
    path('register_new_employees/', views.user_api_view, name='user-api'),
    path('change_user_password/', views.change_password_api_view,
         name='change-user-password'),
]
