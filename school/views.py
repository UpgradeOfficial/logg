from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from school.models import ClassRoom, Expense
from user.models import School
from .serializers import ClassRoomAttendanceModelSerializer, ClassRoomModelSerializer, ExpenseModelSerializer, FeeModelSerializer, SchoolModelSerializer, SubjectModelSerializer, TermModelSerializer
from user import permissions as UserPermission
# Create your views here.


class SchoolListAPIView(ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolModelSerializer
    permission_classes = [permissions.AllowAny]

class ClassRoomListAPIView(ListAPIView):
    serializer_class = ClassRoomModelSerializer
    permission_classes = [permissions.AllowAny]
    

    def get_queryset(self,  *args, **kwargs):
        id = self.kwargs.get('pk')
        return ClassRoom.objects.filter(school_id=id)

class ClassRoomCreateAPIView(CreateAPIView):
    serializer_class = ClassRoomModelSerializer
    permission_classes = [permissions.IsAuthenticated,UserPermission.SchoolPermission]

class ExpenseCreateAPIView(CreateAPIView):
    serializer_class = ExpenseModelSerializer
    permission_classes = [permissions.IsAuthenticated,UserPermission.SchoolPermission]

class ClassRoomAttendanceCreateAPIView(CreateAPIView):
    serializer_class = ClassRoomAttendanceModelSerializer
    permission_classes = [permissions.IsAuthenticated, UserPermission.ClassRoomTeacherPermission]

class FeeCreateAPIView(CreateAPIView):
    serializer_class = FeeModelSerializer
    permission_classes = [permissions.IsAuthenticated, UserPermission.SchoolPermission]   

class SubjectCreateAPIView(CreateAPIView):
    serializer_class = SubjectModelSerializer
    permission_classes = [permissions.IsAuthenticated,UserPermission.SchoolPermission]
    
class TermCreateAPIView(CreateAPIView):
    serializer_class = TermModelSerializer
    permission_classes = [permissions.IsAuthenticated,UserPermission.SchoolPermission]
