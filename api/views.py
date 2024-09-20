from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin, IsSacco, IsCooperative
from authentication.serializers import UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth import authenticate
import logging
from authentication.serializers import UserProfileSerializer



UserProfile = get_user_model()
logger = logging.getLogger(__name__)

# class SignupView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # user.set_password(user.password)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SignupView(APIView):
#     def post(self, request):
#         serializer = UserProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             user.password = make_password(user.password)  # Hash the password
#             user.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)  # Hash the password
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('email')
#         password = request.data.get('password')
#         print(f"^^^^^^^^^^^^^^^^^{username}:::::::::::::::::{password}!!!!!!!!!!!!!!!!!!!!!!!!!111")
#         user = authenticate(request, username=username, password=password)
#         print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!111{user}***************************88")

#         if user is not None:
#             login(request, user)
#             return Response({"message": "Login successful", "role": user.user.role}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             # Generate token logic here
#             return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         print(f"Trying to authenticate user: {username}")  # Debugging line

#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             # Generate tokens
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh)
#             }, status=status.HTTP_200_OK)
        
#         print("Authentication failed!")  # Debugging line
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

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

@csrf_exempt
def generate_token(request):

    user,created =UserProfile.objects.get_or_create(username=' ')

    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        'access':str(refresh.access_token),
        'refresh':str(refresh)
})