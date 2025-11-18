from django.urls import path
from .views import AdminRegisterAPIView, AdminLoginAPIView,AdminUpdateAPIView

urlpatterns = [
    path('register/', AdminRegisterAPIView.as_view(), name='admin-register'),
    path('login/', AdminLoginAPIView.as_view(), name='admin-login'),
    path("update/<int:pk>/", AdminUpdateAPIView.as_view(),name='admin-update'),

]
