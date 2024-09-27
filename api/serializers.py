from rest_framework import serializers
from milkrecords.models import MilkRecords
from farmers.models import FarmersManagement
from cooperative.models import Cooperative
from sacco.models import Sacco
from score.models import Score
from rest_framework import serializers
from users.models import UserProfile
from rest_framework import serializers

class MilkRecordsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='farmer_id.first_name', read_only=True)
    last_name = serializers.CharField(source='farmer_id.last_name', read_only=True)
    farmer_id = serializers.PrimaryKeyRelatedField(queryset=FarmersManagement.objects.all())  

    class Meta:
        model = MilkRecords
        fields = ['farmer_id', 'first_name', 'last_name', 'milk_quantity', 'price', 'date']

class MilkRecordsDetailSerializer(serializers.ModelSerializer):
    total_value = serializers.SerializerMethodField()
    first_name = serializers.CharField(source='farmer_id.first_name', read_only=True)
    last_name = serializers.CharField(source='farmer_id.last_name', read_only=True)

    def get_total_value(self, obj):
        return obj.milk_quantity * obj.price

    class Meta:
        model = MilkRecords
        fields = ['milk_quantity', 'price', 'total_value', 'first_name', 'last_name']


class FarmerDetailSerializer(serializers.ModelSerializer):
    milk_records = MilkRecordsDetailSerializer(many=True, read_only=True)

    class Meta:
        model = FarmersManagement
        fields = ['farmer_id','first_name',"last_name" ,'phone_number', 'cooperative_number', 'created_at']



class FarmersManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmersManagement
        fields = ['farmer_id', 'first_name', 'last_name', 'phone_number', 'cooperative_number', 'sacco_id', 'cooperative_id', 'created_at']
        read_only_fields = ['cooperative_number', 'created_at']  


class SaccoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sacco
        fields = '__all__'


class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = '__all__'        


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Score
        fields="__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        extra_kwargs = {'password':{'write_only': True}}
