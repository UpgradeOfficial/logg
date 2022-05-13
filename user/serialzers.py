from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['groups','user_permissions']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
        

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
        return data
        
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