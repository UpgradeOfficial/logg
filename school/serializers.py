from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import ClassRoom
from user.models import  School
from user.serialzers import UserProfileSerializer

class SchoolModelSerializer(serializers.ModelSerializer):
    user =  UserProfileSerializer()
    class Meta:
        model = School
        fields = '__all__'
        
class ClassRoomModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'  