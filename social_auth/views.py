from os import stat
from telnetlib import STATUS
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializers


# Create your views here.
class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializers

    def post(self, request):
        serializer = self.serializer_class(request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)