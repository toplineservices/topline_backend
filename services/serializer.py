from rest_framework import serializers
from .models import ServiceModels ,ContactUs,Career,JobApplication,Video,Gallery,Blog



class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'excerpt', 'content', 'thumbnail', 'slug','published_date']
        read_only_fields = ['slug']

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = "__all__"

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'youtubeUrl', 'video_file', 'created_at']
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceModels
        fields = '__all__'
        
class ContactUsSerializer(serializers.ModelSerializer):
    
    service_name = serializers.CharField(source='service.name',read_only=True)
    class Meta:
        model = ContactUs
        fields = ['id','firstName','lastName','email','phone','service','service_name','message']


class CareerSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Career
        fields = [
            'id',
            'title',
            'department',
            'location',
            'type',
            'type_display',
            'salary',
            'description',
            'requirements'
        ]
        
class JobApplicationSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career.title', read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'message',
            'resume',
            'applied_at',
            'career',        
            'career_title',  
        ]
        def get_resume(self, obj):
            request = self.context.get('request')
            if obj.resume:
                return request.build_absolute_uri(obj.resume.url)  # full URL
            return None