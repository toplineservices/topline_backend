from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        contacus = ContactUs.objects.all().order_by("-id")
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(contacus, request)
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
