from rest_framework import serializers
from .models import Admin

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Admin
        fields = ['id', 'name', 'email', 'designation', 'password']

    def create(self, validated_data):
        return Admin.objects.create_user(**validated_data)
