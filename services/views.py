from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from django.conf import settings
from .models import (
    Blog,
    ServiceModels,
    ContactUs,
    Career,
    JobApplication,
    Video,
    Gallery,
)
from .serializer import (
    BlogSerializer,
    ServiceSerializer,
    ContactUsSerializer,
    CareerSerializer,
    JobApplicationSerializer,
    VideoSerializer,
    GallerySerializer,
)
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
import datetime

class PaginatedBlogListAPIView(APIView):
    def get(self, request):
        applications = Blog.objects.all().order_by("-published_date")
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(applications, request)
        serializer = BlogSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class BlogListCreateAPIView(APIView):
    def get(self, request):
        blogs = Blog.objects.all().order_by("-published_date")
        serializer = BlogSerializer(blogs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogDetailAPIView(APIView):
    def get(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        serializer = BlogSerializer(blog, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        serializer = BlogSerializer(blog, data=request.data, partial=True)  # partial=True allows updating some fields
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        blog.delete()
        return Response({"message":"item deleted"},status=status.HTTP_204_NO_CONTENT)
class GalleryAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        galleries = Gallery.objects.all().order_by("-created_at")
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(galleries, request)
        serializer = GallerySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryAllImages(APIView):
    def get(self, request):
        galleries = Gallery.objects.filter(event=False).order_by("-created_at")
        serializer = GallerySerializer(galleries, many=True)
        return Response(serializer.data)
class EventImagesAPIView(APIView):
    def get(self, request):
        event_images = Gallery.objects.filter(event=True).order_by("-created_at")
        serializer = GallerySerializer(event_images, many=True)
        return Response(serializer.data)

class GalleryDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    # GET single gallery
    def get(self, request, pk):
        gallery = get_object_or_404(Gallery, pk=pk)
        serializer = GallerySerializer(gallery)
        return Response(serializer.data)

    # PUT - Update gallery
    def put(self, request, pk):
        gallery = get_object_or_404(Gallery, pk=pk)
        serializer = GallerySerializer(gallery, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE - Delete gallery
    def delete(self, request, pk):
        gallery = get_object_or_404(Gallery, pk=pk)
        gallery.delete()
        return Response(
            {"message": "Gallery deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class VideoListCreateAPIView(APIView):
    def get(self, request):
        videos = Video.objects.all().order_by("-created_at")
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetallPaginated(APIView):
    def get(self, request):
        applications = Video.objects.all().order_by("-created_at")
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(applications, request)
        serializer = VideoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class VideoDetailAPIView(APIView):
    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        serializer = VideoSerializer(video)
        return Response(serializer.data)

    def put(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobApplicationAPIView(APIView):
    def get(self, request):
        applications = (
            JobApplication.objects.all()
            .select_related("career")
            .order_by("-applied_at")
        )
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(applications, request)
        serializer = JobApplicationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Application submitted successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobApplicationDetailAPIView(APIView):
    def get(self, request, pk):
        application = get_object_or_404(
            JobApplication.objects.select_related("career"), pk=pk
        )
        serializer = JobApplicationSerializer(application, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        application = get_object_or_404(JobApplication, pk=pk)
        application.delete()
        return Response(
            {"message": "Application deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class JobOpeningAPIView(APIView):
    def get(self, request):
        jobs = Career.objects.all().order_by("-created_at")
        serializer = CareerSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CareerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobListPageAPIView(APIView):
    def get(self, request):
        job = Career.objects.all().order_by("-created_at")
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(job, request)
        serializer = CareerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CareerDetailAPIView(APIView):
    def get(self, request, pk):
        job = get_object_or_404(Career, pk=pk)
        serializer = CareerSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        job = get_object_or_404(Career, pk=pk)
        serializer = CareerSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        job = get_object_or_404(Career, pk=pk)
        serializer = CareerSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = get_object_or_404(Career, pk=pk)
        job.delete()
        return Response(
            {"message": "Job deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class ServiceCreatListAPIView(APIView):
    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        data = ServiceModels.objects.all()
        serializer = ServiceSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class ContactListCreateAPIView(APIView):
    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()

            service_name = contact.service.name if contact.service else "General Inquiry"
            
            # Check for urgent inquiries
            urgent_keywords = ['urgent', 'asap', 'emergency', 'immediately', 'critical']
            is_urgent = any(keyword in contact.message.lower() for keyword in urgent_keywords) or \
                       any(keyword in service_name.lower() for keyword in urgent_keywords)

            # Define 'now' before using it
            now = timezone.localtime(timezone.now())
            
            context = {
                'first_name': contact.firstName,
                'last_name': contact.lastName,
                'email': contact.email,
                'phone': contact.phone,
                'service_name': service_name,
                'message': contact.message,
                'timestamp': now.strftime("%B %d, %Y at %I:%M %p"),  # Now 'now' is defined
                'is_urgent': is_urgent,
            }

            # Use your branded template
            html_message = render_to_string('emails/contact_form_modern.html', context)
            
            subject = f"New Contact: {contact.firstName} {contact.lastName} - {service_name}"
            if is_urgent:
                subject = f"🚨 URGENT: {subject}"

            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['athulraihan27@gmail.com']

            try:
                email = EmailMessage(
                    subject=subject,
                    body=html_message,
                    from_email=from_email,
                    to=recipient_list,
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)
                
            except Exception as e:
                return Response(
                    {"detail": f"Saved but email sending failed: {str(e)}"},
                    status=status.HTTP_201_CREATED
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        contacts = ContactUs.objects.all().order_by("-id")
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(contacts, request)
        serializer = ContactUsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



class ServiceUpdateDropLISTAPIView(APIView):
    def delete(self, request, pk):
        service = get_object_or_404(ContactUs, pk=pk)
        service.delete()
        return Response(
            {"detail": "Contact deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    def get(self, request, pk):
        contact = get_object_or_404(ContactUs, pk=pk)
        serializer = ContactUsSerializer(contact)
        return Response(serializer.data, status=status.HTTP_200_OK)
