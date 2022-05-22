from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from school.models import ClassRoom
from user.models import School
from .serializers import ClassRoomModelSerializer, SchoolModelSerializer
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
    
    


