from rest_framework import serializers
from milkrecords.models import MilkRecords
from farmers.models import FarmersManagement
from score.models import Score

class MilkRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkRecords
        fields = ['farmer_id', 'milk_quantity', 'price', 'date']

class MilkRecordsDetailSerializer(serializers.ModelSerializer):
    total_value = serializers.SerializerMethodField()
    def get_total_value(self, obj):
        return obj.milk_quantity * obj.price
    class Meta:
        model = MilkRecords
        fields = ['milk_quantity', 'price', 'total_value']

class FarmerDetailSerializer(serializers.ModelSerializer):
    milk_records = MilkRecordsDetailSerializer(many=True, read_only=True)

    class Meta:
        model = FarmersManagement
        fields = ['first_name',"last_name" ,'phone_number', 'cooperative_number', 'created_at']

class FarmersManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmersManagement
        fields = ['first_name',"last_name" ,'phone_number', 'cooperative_number', 'created_at']

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Score
        fields="__all__"
