from django.urls import path
from .views import ServiceCreatListAPIView,ContactListCreateAPIView,ServiceUpdateDropLISTAPIView

urlpatterns = [
    path('services',ServiceCreatListAPIView.as_view()),
    path('contact',ContactListCreateAPIView.as_view()),
    
    path('contact/<int:pk>',ServiceUpdateDropLISTAPIView.as_view()),
    
    
    
    
]
