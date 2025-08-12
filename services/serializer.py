from rest_framework import serializers
from .models import ServiceModels ,ContactUs
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceModels
        fields = '__all__'
        
class ContactUsSerializer(serializers.ModelSerializer):
    
    service_name = serializers.CharField(source='service.name',read_only=True)
    class Meta:
        model = ContactUs
        fields = ['id','firstName','lastName','email','phone','service','service_name','message']
        