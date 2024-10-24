from django.urls import path


from . import views

urlpatterns = [
    path('login/', views.user_api_view, name='user-api'),
]
