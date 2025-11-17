from rest_framework import serializers
from .models import Admin

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Admin
        fields = ['id', 'name', 'email', 'designation', 'password', 'profile_image']

    def update(self, instance, validated_data):
        # Update basic fields
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.designation = validated_data.get('designation', instance.designation)

        # Handle profile image
        if validated_data.get('profile_image'):
            instance.profile_image = validated_data.get('profile_image')

        # Handle password only if provided
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def create(self, validated_data):
        return Admin.objects.create_user(**validated_data)
