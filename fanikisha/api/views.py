from django.shortcuts import render

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from score.models import Score
from .ml_model import predict_credit_score
from rest_framework.response import Response
from farmers.models import  FarmersManagement
from milkrecords.models import MilkRecords
from .serializers import  FarmersManagementSerializer, MilkRecordsSerializer, MilkRecordsDetailSerializer, FarmerDetailSerializer,ScoreSerializer
from django.shortcuts import get_object_or_404
import logging

class FarmersManagementListView(APIView):
    def get(self, request):
        farmers = FarmersManagement.objects.all()
        serializer = FarmersManagementSerializer(farmers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
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
        serializer = MilkRecordsSerializer(milk_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MilkRecordsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MilkRecordsDetailView(APIView):
    def get(self, request, farmers_id):
        try:
            milk_records = FarmersManagement.objects.get(pk=farmers_id)
        except FarmersManagement.DoesNotExist:
            return Response({"detail": "Farmer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        milk_records = MilkRecords.objects.filter(farmer_id=farmers_id)
        serializer = MilkRecordsDetailSerializer(milk_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, farmers_id):
        try:
            milk_record = FarmersManagement.objects.get(pk=farmers_id)
        except FarmersManagement.DoesNotExist:
            return Response({"detail": "Farmer not found."}, status=status.HTTP_404_NOT_FOUND)

        record_id = request.data.get('record_id')
        try:
            milk_record = MilkRecords.objects.get(pk=record_id, farmer_id=farmers_id)
        except MilkRecords.DoesNotExist:
            return Response({"detail": "Milk record not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MilkRecordsSerializer(milk_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



logger = logging.getLogger(__name__)

class ScoreDetailView(APIView):
    def get(self, request, farmer_id):
        try:
            farmer_instance = get_object_or_404(Farmer, farmer_id=farmer_id)
            
            try:
                score_instance = Score.objects.get(farmer=farmer_instance)
            except Score.DoesNotExist:
                logger.warning(f"No score found for farmer {farmer_id}")
                return Response({'error': 'No score found for this farmer'}, status=status.HTTP_404_NOT_FOUND)

#I should have a farmer's data that will be passed to the ml model
#I call the ml model to predict the score
#I create a new score instance if it exists I continue 

            if self.is_prediction_outdated(score_instance):
                try:
                    ml_prediction = predict_credit_score(farmer_id)
                    score_instance.score = ml_prediction['score']
                    score_instance.credit_worthiness = ml_prediction['credit_worthiness']
                    score_instance.loan_range = ml_prediction['loan_range']
                    score_instance.last_checked_date = timezone.now()
                    score_instance.status = ml_prediction['status']
                    score_instance.save()
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

        except FarmersManagement.DoesNotExist:
            logger.warning(f"Farmer not found: {farmer_id}")
            return Response({'error': 'Farmer not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error for farmer {farmer_id}: {str(e)}")
            return Response({'error': 'Farmer not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


