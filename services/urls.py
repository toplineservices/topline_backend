from django.urls import path
from .views import (
    ServiceCreatListAPIView,
    ContactListCreateAPIView,
    ServiceUpdateDropLISTAPIView,
    JobOpeningAPIView,
    JobListPageAPIView,
    CareerDetailAPIView,
    JobApplicationAPIView,
    JobApplicationDetailAPIView,
    VideoDetailAPIView,
    VideoListCreateAPIView,
    GetallPaginated,
    GalleryAPIView,
    GalleryDetailAPIView,
    GalleryALLImages
)

urlpatterns = [
    path("services", ServiceCreatListAPIView.as_view()),
    path("contact", ContactListCreateAPIView.as_view()),
    path("contact/<int:pk>", ServiceUpdateDropLISTAPIView.as_view()),
    path("career", JobOpeningAPIView.as_view(), name="job-openings"),
    path("careerlist", JobListPageAPIView.as_view(), name="job-openings"),
    path("careers/<int:pk>", CareerDetailAPIView.as_view(), name="job-detail"),
    path("applications", JobApplicationAPIView.as_view(), name="job-applications"),
    path(
        "applications/<int:pk>",
        JobApplicationDetailAPIView.as_view(),
        name="job-applications",
    ),
    path("videos", VideoListCreateAPIView.as_view(), name="video-list-create"),
    path("video", GetallPaginated.as_view(), name="video-list-create"),
    path("videos/<int:pk>", VideoDetailAPIView.as_view(), name="video-detail"),
    path("galleries", GalleryAPIView.as_view(), name="gallery-list-create"),
    path("galleriespage/<int:pk>", GalleryDetailAPIView.as_view(), name="gallery-detail"),
    path("galleriesallimage", GalleryALLImages.as_view(), name="gallery-list-create"),
    
    
]
