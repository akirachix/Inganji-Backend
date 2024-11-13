from rest_framework import serializers
from api import models
from milkrecords.models import MilkRecords
from farmers.models import FarmersManagement
from cooperative.models import Cooperative
from sacco.models import Sacco
from score.models import Score
from users.models import UserProfile
from django.db.models import Sum, F

from rest_framework import serializers
from django.db.models import Sum


class MilkRecordsSerializer(serializers.ModelSerializer):
    # total_value = serializers.SerializerMethodField()
    total_milk_value = serializers.SerializerMethodField()  
    first_name = serializers.CharField(source='farmer_id.first_name', read_only=True)
    last_name = serializers.CharField(source='farmer_id.last_name', read_only=True)
    farmer_id = serializers.PrimaryKeyRelatedField(queryset=FarmersManagement.objects.all())  
    def get_total_value(self, obj):
        return obj.milk_quantity * obj.price

    def get_total_milk_value(self, obj):
        total = MilkRecords.objects.filter(farmer_id=obj.farmer_id).aggregate(
            total_value=Sum('milk_quantity') * Sum('price')
        )['total_value']
        return total
     
    class Meta:
        model = MilkRecords
        fields = ['farmer_id', 'first_name', 'last_name', 'milk_quantity', 'price', 'date',"total_milk_value"]

class MilkRecordsDetailSerializer(serializers.ModelSerializer):
    total_value = serializers.SerializerMethodField()
    total_milk_value = serializers.SerializerMethodField()  
    first_name = serializers.CharField(source='farmer_id.first_name', read_only=True)
    last_name = serializers.CharField(source='farmer_id.last_name', read_only=True)

    def get_total_value(self, obj):
        total_value = MilkRecords.objects.filter(farmer_id=obj.farmer_id) \
        .aggregate(total=Sum(F('milk_quantity') * F('price')))['total']
        return total_value


    def get_total_milk_value(self, obj):
        total = MilkRecords.objects.filter(farmer_id=obj.farmer_id).aggregate(
            total_value=Sum('milk_quantity') * Sum('price')
        )['total_value']
        return total

    class Meta:
        model = MilkRecords
        fields = ['milk_quantity', 'price', 'total_value', 'total_milk_value', 'first_name', 'last_name']


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



class LoanEligibilityInputSerializer(serializers.Serializer):
    owns_car = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')])
    owns_property = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')])
    num_children = serializers.IntegerField()
    total_income = serializers.FloatField()
    education_type = serializers.CharField(max_length=50)
    family_status = serializers.CharField(max_length=50)
    housing_type = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    employment_duration = serializers.FloatField()
    occupation_type = serializers.CharField(max_length=50)
    number_of_family_members = serializers.IntegerField()
    total_dependents = serializers.IntegerField()
    household_size = serializers.IntegerField()
    is_long_employment = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')])
