from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Admin
from .serializer import AdminSerializer
from .utils import get_tokens_for_user
from django.shortcuts import get_object_or_404
class AdminRegisterAPIView(APIView):
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save()
            return Response({
                "message": "Admin registered successfully",
                "admin": AdminSerializer(admin).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user:
            token = get_tokens_for_user(user)
            return Response({
                "message": "Login successful",
                "token": token,
                "admin": AdminSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

class AdminUpdateAPIView(APIView):

    def put(self, request, pk):
        admin = get_object_or_404(Admin, pk=pk)
        serializer = AdminSerializer(admin, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Admin updated successfully",
                "admin": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

