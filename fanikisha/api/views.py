from django.shortcuts import render

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from farmers.models import  FarmersManagement
from milkrecords.models import MilkRecords
from .serializers import  FarmersManagementSerializer, MilkRecordsSerializer, MilkRecordsDetailSerializer, FarmerDetailSerializer


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


