from django.urls import path
from .views import AdminRegisterAPIView, AdminLoginAPIView

urlpatterns = [
    path('register/', AdminRegisterAPIView.as_view(), name='admin-register'),
    path('login/', AdminLoginAPIView.as_view(), name='admin-login'),
]
