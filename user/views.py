from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from core.utils import jwt_decode, jwt_encode

from .models import User
from .serialzers import ForgotPasswordSerializer, ChangePasswordSerializer, ResetPasswordSerializer

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




    
    
