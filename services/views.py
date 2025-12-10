from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from django.conf import settings
import logging
from django.db.models import Q
from .models import (
    Blog,
    ServiceModels,
    ContactUs,
    Career,
    JobApplication,
    Video,
    Gallery,
    SiteVisit
    
)
from .serializer import (
    BlogSerializer,
    ServiceSerializer,
    ContactUsSerializer,
    CareerSerializer,
    JobApplicationSerializer,
    VideoSerializer,
    GallerySerializer,
    SiteVisitSerializer
)
from django.db.models import Count
from django.db.models.functions import TruncMonth
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
import calendar
from datetime import date
logger = logging.getLogger(__name__)
from datetime import datetime

class TotalVisitsAndContactsAPIView(APIView):
    """
    Returns total counts for SiteVisit and ContactUs
    """
    def get(self, request):
        total_visits = SiteVisit.objects.count()
        total_contacts = ContactUs.objects.count()
        total_jobs = Career.objects.count()

        return Response({
            "total_visits": total_visits,
            "total_contacts": total_contacts,
            "total_jobs": total_jobs
        })
class TrackVisitView(APIView):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        ip = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        SiteVisit.objects.create(ip_address=ip, user_agent=user_agent)
        return Response({"message": "Visit recorded successfully"})

    def get(self, request):
        visits = SiteVisit.objects.all().order_by('-visited_at')
        serializer = SiteVisitSerializer(visits, many=True)
        return Response(serializer.data)
class VisitCountView(APIView):
    def get(self, request):
        today = date.today()
        current_year = today.year
        current_month = today.month

        # Aggregate visits by month
        visits = (
            SiteVisit.objects
            .filter(visited_at__year=current_year)
            .annotate(month=TruncMonth('visited_at'))
            .values('month')
            .annotate(visits=Count('id'))
            .order_by('month')
        )

        # Initialize past months with 0
        month_data = {}
        for i in range(1, current_month + 1):  # only past and current months
            month_abbr = calendar.month_abbr[i]
            month_data[month_abbr] = 0

        # Fill in actual data
        for v in visits:
            month_str = v['month'].strftime('%b')
            if month_str in month_data:
                month_data[month_str] = v['visits']

        # Convert to list of dicts
        data = [{'month': month, 'visits': month_data[month]} for month in month_data]

        return Response(data)


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

        search = request.query_params.get('search', None)
        published_date = request.query_params.get('published_date', None)
        blogs = Blog.objects.all()
    
        if search:
            blogs = blogs.filter(
                Q(title__icontains=search) |
                Q(excerpt__icontains=search) |
                Q(content__icontains=search) |
                Q(author__icontains=search)
            )
    

        if published_date:
            try:
                filter_date = datetime.strptime(published_date, '%Y-%m-%d').date()
                blogs = blogs.filter(published_date=filter_date)
            except ValueError:
                pass
    
    
        blogs = blogs.order_by("-published_date")
    
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
        job = request.GET.get("job")
        name = request.GET.get("name")
        date = request.GET.get("date")

        if job:
            applications = applications.filter(career__title__icontains=job)

        if name:
            applications = applications.filter(first_name__icontains=name)

        if date:
            applications = applications.filter(applied_at__date=date)

        paginator = PageNumberPagination()
        paginator.page_size = int(request.GET.get("pageSize", 10))
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

class MonthlyContactsReportAPIView(APIView):
    """
    Returns monthly contact submissions report
    """
    def get(self, request):
        today = date.today()
        current_year = today.year
        current_month = today.month

        # Aggregate contacts by month for current year
        contacts = (
            ContactUs.objects
            .filter(created_at__year=current_year)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(contacts=Count('id'))
            .order_by('month')
        )

        # Initialize months with 0
        month_data = {calendar.month_abbr[i]: 0 for i in range(1, current_month + 1)}

        # Fill in actual data
        for c in contacts:
            month_str = c['month'].strftime('%b')
            if month_str in month_data:
                month_data[month_str] = c['contacts']

        # Convert to list of dicts
        data = [{'month': month, 'contacts': month_data[month]} for month in month_data]

        return Response(data)


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

            now = timezone.localtime(timezone.now())
            
            context = {
                'first_name': contact.firstName,
                'last_name': contact.lastName,
                'email': contact.email,
                'phone': contact.phone,
                'service_name': service_name,
                'message': contact.message,
                'timestamp': now.strftime("%B %d, %Y at %I:%M %p"),
                'is_urgent': is_urgent,
            }

            html_message = render_to_string('emails/contact_form_modern.html', context)
            
            subject = f"New Contact: {contact.firstName} {contact.lastName} - {service_name}"
            if is_urgent:
                subject = f"🚨 URGENT: {subject}"

            from_email = settings.EMAIL_HOST_USER
            # recipient_list = [email.strip() for email in settings.CONTACT_RECIPIENTS if email.strip()]
            recipient_list = ['sudhir.kg@toplineservices.in','gkmathew@toplineservices.in','ps@toplineservices.in','Info@toplineservices.in']

            
            logger.info(f"Contact form submitted  to {recipient_list}.")

            try:

                email = EmailMessage(
                    subject=subject,
                    body=html_message,
                    from_email=from_email,
                    to=recipient_list,
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)
      
                logger.info(f"Contact form submitted by {contact.email} for service '{service_name}'.")
                if is_urgent:
                    logger.warning(f"⚠️ Urgent inquiry received from {contact.email}.")
                
            except Exception as e:
                logger.error(f"Failed to send email for contact {contact.email}: {e}", exc_info=True)
                return Response(
                    {"detail": f"Saved but email sending failed: {str(e)}"},
                    status=status.HTTP_201_CREATED
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"Invalid contact form submission: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        contacts = ContactUs.objects.all().order_by("-id")

        name = request.GET.get("name")
        email = request.GET.get("email")
        date = request.GET.get("date")

        if name:
            contacts = contacts.filter(firstName__icontains=name)

        if email:
            contacts = contacts.filter(email__icontains=email)

        if date:
            contacts = contacts.filter(created_at__date=date)

        paginator = PageNumberPagination()
        paginator.page_size = int(request.GET.get("pageSize", 10))
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
