from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin, IsSacco, IsCooperative
from authentication.serializers import UserProfileSerializer
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth import authenticate
import logging
from authentication.serializers import UserProfileSerializer



UserProfile = get_user_model()
logger = logging.getLogger(__name__)

class SignupView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)  # Hash the password
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # refresh = RefreshToken.for_user(user)
            return Response({
                "message": "logged right"
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "This is an admin-only view."})

class SaccoOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsSacco]

    def get(self, request):
        return Response({"message": "This is a SACCO-only view."})

class CooperativeOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsCooperative]

    def get(self, request):
        return Response({"message": "This is a cooperative-only view."})
