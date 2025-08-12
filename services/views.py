from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ServiceModels ,ContactUs
from .serializer import ServiceSerializer ,ContactUsSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

class ServiceCreatListAPIView(APIView):
    def post(self,request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self,request):
        data = ServiceModels.objects.all()
        serializer = ServiceSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ContactListCreateAPIView(APIView):
    def post(self,request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        contacus = ContactUs.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(contacus, request)
        serializer = ContactUsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)  

class ServiceUpdateDropLISTAPIView(APIView):
    def delete(self,request,pk):
        service = get_object_or_404(ContactUs,pk=pk)
        service.delete()
        return Response({"detail": "Contact deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    def get(self,request,pk):
        contact = get_object_or_404(ContactUs,pk=pk)
        serializer = ContactUsSerializer(contact)
        return Response(serializer.data,status=status.HTTP_200_OK)