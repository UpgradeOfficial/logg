from asyncio.log import logger
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import ClassRoom, ClassRoomAttendance, Expense, Fee, Subject, Term
from user.models import  School
from user.serialzers import UserProfileSerializer

class SchoolModelSerializer(serializers.ModelSerializer):
    user =  UserProfileSerializer()
    class Meta:
        model = School
        fields = '__all__'
        
class ClassRoomModelSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)
    class Meta:
        model = ClassRoom
        fields = '__all__'

class ExpenseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class ClassRoomAttendanceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoomAttendance
        fields = '__all__'
        
class FeeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'

class TermModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'

class SubjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


