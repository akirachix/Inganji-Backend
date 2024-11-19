from datetime import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response
from farmers.models import  FarmersManagement
from milkrecords.models import MilkRecords
from cooperative.models import Cooperative
from sacco.models import Sacco
from .serializers import  FarmersManagementSerializer, MilkRecordsSerializer, MilkRecordsDetailSerializer, FarmerDetailSerializer,CooperativeSerializer, SaccoSerializer ,ScoreSerializer
from score.models import Score
from .ml_model import predict_credit_score
from django.shortcuts import get_object_or_404
import logging
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin, IsSacco, IsCooperative
from .serializers import UserProfileSerializer
from .serializers import UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate
import logging
from .serializers import UserProfileSerializer
from .serializers import ScoreSerializer
from django.utils import timezone


class FarmersManagementListView(APIView):
    def get(self, request):
        cooperative_id = request.query_params.get('cooperative_id', None)
        sacco_id = request.query_params.get('sacco_id', None)

        farmers = FarmersManagement.objects.all()

        if cooperative_id:
            farmers = farmers.filter(cooperative_id=cooperative_id)
        
        if sacco_id:
            farmers = farmers.filter(sacco_id=sacco_id)

        count = farmers.count()
        serializer = FarmersManagementSerializer(farmers, many=True)
        return Response({
            'count': count,
            'farmers': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        cooperative_id = request.data.get('cooperative_id')
        if not Cooperative.objects.filter(cooperative_id=cooperative_id).exists():
            return Response({"error": "Invalid cooperative ID"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FarmersManagementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FarmersManagementDetailView(APIView):
    def get(self, request, farmer_id):
        try:
            farmer = FarmersManagement.objects.get(pk=farmer_id)
        except FarmersManagement.DoesNotExist:
            return Response({"detail": f"Farmer with ID {farmer_id} does not exist in our records. Please ensure the ID is correct and try again."
}, status=status.HTTP_404_NOT_FOUND)
        serializer = FarmersManagementSerializer(farmer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, farmer_id):
        try:
            farmer = FarmersManagement.objects.get(pk=farmer_id)
        except FarmersManagement.DoesNotExist:
            return Response({"detail": "Farmer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FarmersManagementSerializer(farmer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class MilkRecordsListView(APIView):
    def get(self, request):
        milk_records = MilkRecords.objects.all()
        unique_records = {}
        for record in milk_records:
            identifier = (record.farmer_id.farmer_id)  
            if identifier not in unique_records:
                unique_records[identifier] = record
            else:
                if record.milk_quantity > unique_records[identifier].milk_quantity:
                    unique_records[identifier] = record

        unique_records_list = list(unique_records.values())
        serializer = MilkRecordsSerializer(unique_records_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MilkRecordsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MilkRecordsDetailView(APIView):
    def get(self, request, farmer_id):
        try:
            milk_records = FarmersManagement.objects.get(pk=farmer_id)
        except FarmersManagement.DoesNotExist:
            return Response({"detail": "Farmer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        milk_records = MilkRecords.objects.filter(farmer_id=farmer_id)
        serializer = MilkRecordsDetailSerializer(milk_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, farmer_id):
        try:
            milk_record = FarmersManagement.objects.get(pk=farmer_id)
        except FarmersManagement.DoesNotExist:
            return Response({"detail": "Farmer not found."}, status=status.HTTP_404_NOT_FOUND)

        record_id = request.data.get('record_id')
        try:
            milk_record = MilkRecords.objects.get(pk=record_id, farmer_id=farmer_id)
        except MilkRecords.DoesNotExist:
            return Response({"detail": "Milk record not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MilkRecordsSerializer(milk_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaccoList(generics.ListCreateAPIView):
    serializer_class = SaccoSerializer

    def get_queryset(self):
        return Sacco.objects.all()

    def get(self, request):
        sacco = self.get_queryset()
        serializer = self.get_serializer(sacco, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaccoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SaccoSerializer

    def get_object(self, pk):
        try:
            return Sacco.objects.get(pk=pk)
        except Sacco.DoesNotExist:
            raise Http404("Sacco not found")

    def get(self, request, sacco_id):
        sacco = self.get_object(sacco_id)
        serializer = self.get_serializer(sacco)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class CooperativeList(generics.ListCreateAPIView):
    serializer_class = CooperativeSerializer

    def get_queryset(self):
        return Cooperative.objects.all()

    def get(self, request):
        cooperative = self.get_queryset()
        serializer = self.get_serializer(cooperative, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
logger = logging.getLogger(__name__)


class ScoreDetailView(APIView):
    def get(self, request, farmer_id):
        farmer_instance = get_object_or_404(FarmersManagement, farmer_id=farmer_id)
        logger.info(f"Fetched farmer: {farmer_instance}")

        try:
            score_instance = Score.objects.get(farmer_id=farmer_instance) 
            logger.info(f"Fetched score for farmer {farmer_id}: {score_instance}")
        except Score.DoesNotExist:
            logger.warning(f"No score found for farmer {farmer_id}")
            return Response({'error': 'No score found for this farmer'}, status=status.HTTP_404_NOT_FOUND)

        if self.is_prediction_outdated(score_instance):
            try:
                ml_prediction = predict_credit_score(farmer_id)
                logger.info(f"ML Prediction for farmer {farmer_id}: {ml_prediction}")

                score_instance.score = ml_prediction['score']
                score_instance.credit_worthiness = ml_prediction['credit_worthiness']
                score_instance.loan_range = ml_prediction['loan_range']
                score_instance.last_checked_date = timezone.now().date()
                score_instance.is_eligible = ml_prediction['is_eligible']
                score_instance.save()
                logger.info(f"Score updated for farmer {farmer_id}.")
            except KeyError as ke:
                logger.error(f"KeyError: {str(ke)} - Ensure that all necessary fields are in the prediction response.")
                return Response({'error': f'Missing field in prediction: {str(ke)}'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Error updating prediction for farmer {farmer_id}: {str(e)}")
                return Response({'error': 'Error updating prediction'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ScoreSerializer(score_instance)

        if 'credit_score' in request.query_params:
            return Response({'credit_score': serializer.data['score']})
        elif 'creditworthiness' in request.query_params:
            return Response({'creditworthiness': serializer.data['credit_worthiness']})
        elif 'loan_range' in request.query_params:
            return Response({'loan_range': serializer.data['loan_range']})
        else:
            return Response(serializer.data)

    def is_prediction_outdated(self, score_instance):
        return timezone.now().date() > score_instance.last_checked_date


class ScoreListView(APIView):
    """
    API View for getting a list of Scores.
    You can filter Scores by farmer_id.
    """
    
    def get(self, request):
        scores = self.get_queryset()
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Score.objects.all()
        farmer_id = self.request.query_params.get('farmer_id', None)
        

        if farmer_id:
            queryset = queryset.filter(farmer__farmer_id=farmer_id)
            
        return queryset

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
            return Response({
                "message": "Successful Log In"
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


class ScoreCreateView(APIView):
    def post(self, request):
        farmer_id = request.data.get('farmer_id')
        
        try:
            farmer = FarmersManagement.objects.get(farmer_id=farmer_id)
        except FarmersManagement.DoesNotExist:
            return Response({'error': 'Farmer not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ScoreSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Score created successfully!', 'score_id': serializer.instance.credit_score_id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


import pickle
import pandas as pd
from django.http import JsonResponse
from django.views import View
from predictive_model.models import Prediction
import json
from datetime import datetime

class PredictLoanEligibility(View):
    education_type_mapping = {
        'Primary': 1,
        'Secondary': 2,
        'Higher': 3,
        'Postgraduate': 4
    }
    
    family_status_mapping = {
        'Single': 0,
        'Married': 1,
        'Divorced': 2,
        'Widowed': 3,
        'Separated': 4
    }
    
    housing_type_mapping = {
        'Rent': 0,
        'Own': 1,
        'Mortgage': 2,
        'Other': 3
    }

    def post(self, request):
        model_path = "predictive_model/model/rForest_model.pkl" 
        with open(model_path, "rb") as file:
            model = pickle.load(file)

        try:
            input_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        cleaned_input_data = {
            'owns_car': int(input_data.get('owns_car', 'no') == 'yes'),
            'owns_property': int(input_data.get('owns_property', 'no') == 'yes'),
            'num_children': int(input_data.get('num_children', 0)),
            'total_income': float(input_data.get('total_income', 0)),
            'education_type': self.education_type_mapping.get(input_data.get('education_type', 'unknown'), -1),
            'family_status': self.family_status_mapping.get(input_data.get('family_status', 'unknown'), -1),
            'housing_type': self.housing_type_mapping.get(input_data.get('housing_type', 'unknown'), -1),
            'age': int(input_data.get('age', 0)),
            'employment_duration': int(input_data.get('employment_duration', 0)),
            'number_of_family_members': int(input_data.get('number_of_family_members', 0)),
            'total_dependents': int(input_data.get('total_dependents', 0)),
            'is_long_employment': int(input_data.get('is_long_employment', 'no') == 'yes')
        }

        cleaned_input_df = pd.DataFrame([cleaned_input_data])

        features = [
            'owns_car', 'owns_property', 'num_children', 'total_income',
            'education_type', 'family_status', 'housing_type', 'age', 
            'employment_duration', 'number_of_family_members',
            'total_dependents', 'is_long_employment'
        ]
        
        cleaned_input_df = cleaned_input_df[features]

        missing_features = [feature for feature in features if feature not in cleaned_input_df.columns]
        if missing_features:
            return JsonResponse({'error': f"Missing features in input data: {missing_features}"}, status=400)

        try:
            prediction = model.predict(cleaned_input_df)

            eligibility = "Eligible" if prediction[0] == 1 else "Not Eligible" 
            
            current_date = datetime.now().date().isoformat()
            
            Prediction.objects.create(prediction_result=prediction[0], **cleaned_input_data)

            return JsonResponse({
                'prediction': prediction.tolist(),
                'eligibility': eligibility,
                'current_date': current_date
            })
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)


