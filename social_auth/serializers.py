from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.conf import settings

from user.models import User
from .google import Google 
from . import register

class GoogleSocialAuthSerializers(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError("this token has expired or is no longer in use")
        if user_data['aud'] != settings.GOOOGEL_CLIENT_ID:
            raise serializers.ValidationError("opps, who are you !!!")
        
        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = User.AUTH_PROVIDER_TYPE.GOOGLE

        return register.register_social_user(
            provider=provider, user_id=user_id, email=email, name=name
        )