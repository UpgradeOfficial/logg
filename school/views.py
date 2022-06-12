from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from yaml import serialize
from core.utils import send_mail_with_attachment
from school.models import ClassRoom
from user.models import School, Student
from .serializers import AnnouncementModelSerializer, AppointmentModelSerializer, ClassRoomAttendanceModelSerializer, ClassRoomModelSerializer, EmailAttachmentSerializer, ExpenseModelSerializer, FeeModelSerializer, SchoolModelSerializer, SubjectModelSerializer, TermModelSerializer
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

class ClassRoomCreateAPIView(ListCreateAPIView):
    serializer_class = ClassRoomModelSerializer
    permission_classes = [permissions.IsAuthenticated,UserPermission.SchoolPermission]
    

    def get_queryset(self):
        classrooms =ClassRoom.objects.filter(school__user =self.request.user)
        return classrooms
        # if self.request.user.USER_TYPE == User.USER_TYPE.SCHOOL:
        #     return ClassRoom.objects.filter(school__user= self.request.user)


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

class AnnouncementCreateAPIView(CreateAPIView):
    serializer_class = AnnouncementModelSerializer
    permission_classes = [permissions.IsAuthenticated,UserPermission.SchoolPermission]

class AppointmentCreateAPIView(CreateAPIView):
    serializer_class = AppointmentModelSerializer
    permission_classes = [permissions.IsAuthenticated,UserPermission.SchoolPermission]

class SendMailView(APIView):
    '''
    Post a file(Image file) to this endpoint and it will be sent to 
    the Patient mail, the name of the file must be named file
    '''
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmailAttachmentSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data.get('file')
        # email = serializer.validated_data.get('email_dict')
        template_name= "email_attachment.html"
        subject = f"File sent to {user.email}"
        email = [user.email,]
        context={
                'email_sender': user.email
        }
        send_mail_with_attachment(subject=subject, to_email=email, file=file, input_context=context, template_name=template_name,)
        data = { 'message':"email sent successfully"}
        return Response(status=status.HTTP_200_OK,data=data)





