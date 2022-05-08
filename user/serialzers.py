from dataclasses import fields
from urllib import request
from django.forms import PasswordInput
from rest_framework import serializers


class ForgotPasswordSerializer(serializers.Serializer):
    """
    This is used to serializer the email field 
    """
    email = serializers.EmailField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)

    def validate(self, data):
        user = self.context['request'].user
        old_password = data['old_password']
        new_password = data['new_password']
        if user:
            if not user.check_password(old_password):
                raise serializers.ValidationError("The old password field is incorrect")
        if old_password == new_password:
            raise serializers.ValidationError("old password and new password must be different")
        return data

class ResetPasswordSerializer(serializers.Serializer):
    """
    This is used to serializer the password field 
    """
    password = serializers.CharField()