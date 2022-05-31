from asyncio.log import logger
from click import secho
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Announcement, Appointment, ClassRoom, ClassRoomAttendance, Expense, Fee, Subject, Term
from user.models import  School, User
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

class AppointmentModelSerializer(serializers.ModelSerializer):
    #invitee = serializers.UUIDField()
    class Meta:
        model = Appointment
        fields = '__all__'
        extra_kwargs = {'initiator': {'read_only': True}, }


    def create(self, validated_data):
        
        invitee_id = validated_data.pop('invitee')
        initiator = self.context['request'].user
        invitee = get_object_or_404(User, email=invitee_id)
        appointment = Appointment.objects.create(invitee=invitee, initiator=initiator, **validated_data )
        return appointment


class AnnouncementModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Announcement
        fields = '__all__'


