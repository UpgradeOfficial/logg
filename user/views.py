import codecs
import csv
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics, parsers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from core.utils import jwt_decode, jwt_encode
import logging
from rest_framework_simplejwt.views import TokenObtainPairView

from user.utils import create_student_user, download_csv
from .serialzers import MyTokenObtainPairSerializer, StudentSerializer
from core.utils import ExpiringActivationTokenGenerator
from .filters import UserFilter
from .models import Student, User
from .serialzers import (ForgotPasswordSerializer,
                        ChangePasswordSerializer, 
                        ResetPasswordSerializer, 
                        UserProfileSerializer, 
                        UserRegistrationSerializer)

from .permissions import SchoolPermission

logger = logging.getLogger('main')

# Create your views here.
class InitiatePasswordResetView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            payload={'email':email}
            token = jwt_encode(payload)
            # send email to the user with a password reset link
            return Response(status=status.HTTP_200_OK, data={"message": "email sent"})
        
        return Response(status=status.HTTP_400_BAD_REQUEST , data={"message": "user not found"})



class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
        
   
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        password = request.data['new_password']
        if serializer.is_valid(raise_exception=True):
            self.object.set_password(password)
            self.object.save()
            return Response(status=status.HTTP_200_OK, data={"message": "Password changed"})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "bad request"})

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]



    def  patch(self, request, token, *args, **kwargs):
        serializer = ResetPasswordSerializer(data = request.data)
        if serializer.is_valid():
            decoded_data = jwt_decode(token)
            email = decoded_data['email']
            user = get_object_or_404(User, email=email)
            user.set_password(serializer.validated_data.get('password'))
            user.save()
            return Response(status=status.HTTP_200_OK, data={"message":"password reset successful"})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "bad request"})


class UserRegistrationView(generics.CreateAPIView):
    # this can be tested in postman with the form-data
    # Use form data in the client part also
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs):
        
        decoded_data =  ExpiringActivationTokenGenerator().get_token_value(token)
        email = decoded_data
        user = get_object_or_404(User, email=email)
        user.is_verified =True
        user.save()
        return Response(status=status.HTTP_200_OK, data={"message" : "Email Verification successful"})

class UserRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    lookup_field = "id"

class UserListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    filterset_class = UserFilter




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    
    
class UploadStudentView(generics.ListCreateAPIView):
    print('yes')
    permission_classes = [AllowAny, ]
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        print('enteres')
        data = download_csv(Student.objects.all())
        return HttpResponse (data, content_type='text/csv')

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        reader = csv.DictReader(codecs.iterdecode(file, 'utf-8'), delimiter=',')
        data = list(reader)
        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        student_list =[]
        for row in serializer.data:
            user = create_student_user(row['first_name'], row['last_name'])
            student_list.append(
            Student(user=user)
            )

        Student.objects.bulk_create(student_list)
        return Response(status=status.HTTP_201_CREATED, data={"message":"Controlled Substances Uploaded Successfully"})


# @api_view
# def UploadStudentView(request):
#     print('yes')
#     data = download_csv(Student.objects.all())
#     return HttpResponse (data, content_type='text/csv')
