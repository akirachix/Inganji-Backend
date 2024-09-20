from rest_framework import serializers
from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        # extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     role = validated_data.pop('role')
    #     # user = 
    #     user = UserProfile(**validated_data)
    #     user.save()
        
    #     return user