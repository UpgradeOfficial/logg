from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from core.utils import send_mail
from django.conf import settings
from school.models import ClassRoom
from .models import School, Student, User


class UserRegistrationSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()
    classroom = serializers.UUIDField(required=False, write_only=True)
    school = serializers.UUIDField(required=False, write_only=True)
    class Meta:
        model = User
        exclude = ['groups','user_permissions', 'auth_povider'] + User.get_hidden_fields()
        read_only_fields = ('is_active', 'is_staff')
        extra_kwargs = {
            'user_type': {'write_only': True},
            
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        school_id = validated_data.pop('school', None)
        classroom_id = validated_data.pop('classroom', None)
        user = super().create(validated_data)
        if password is None:
            raise serializers.ValidationError("You did not provide a valid password")
        user.set_password(password)
        user.save()
        if validated_data.get('user_type', User.USER_TYPE.STUDENT) == User.USER_TYPE.STUDENT:
            school = get_object_or_404(School, id=school_id)
            classroom = get_object_or_404(ClassRoom, id=classroom_id)
            Student.objects.create(user=user, school=school, classroom=classroom)
        elif validated_data.get('user_type') == User.USER_TYPE.SCHOOL:
            School.objects.create(user=user)
        
        context = {
            'name':user.first_name or "Guest",
            'link': "https://nairaland.com/",
            'site': "Logg",
            'MEDIA_URL': 'media/'
        }
        send_mail(subject="Welcome To Logg", to_email=user.email, input_context=context, template_name='account_verification.html', cc_list=[], bcc_list=[])
        return user
        

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
        return data
class UserProfileSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        exclude = ['groups','user_permissions', "password"]

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