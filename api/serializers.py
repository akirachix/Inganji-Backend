from rest_framework import serializers
from milkrecords.models import MilkRecords
from farmers.models import FarmersManagement
from cooperative.models import Cooperative
from sacco.models import Sacco
from score.models import Score
from rest_framework import serializers
from users.models import UserProfile

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
        fields = ['farmer_id','first_name',"last_name" ,'phone_number', 'cooperative_number', 'created_at']



class FarmersManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmersManagement
        fields = ['farmer_id', 'first_name', 'last_name', 'phone_number', 'cooperative_number', 'sacco_name', 'cooperative_id', 'created_at']
        read_only_fields = ['cooperative_number', 'created_at']  

    def create(self, validated_data):
        
        farmer = FarmersManagement(**validated_data)
        farmer.save()  
        return farmer

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.sacco_name = validated_data.get('sacco_name', instance.sacco_name)
        instance.cooperative_id = validated_data.get('cooperative_id', instance.cooperative_id)

        if instance.cooperative_id != validated_data.get('cooperative_id'):
            instance.cooperative_number = instance.generate_cooperative_number()

        instance.save()  
        return instance


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
