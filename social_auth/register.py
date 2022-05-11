from turtle import Turtle
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

def register_social_user(provider, user_id, email, name):
    filter_user_by_email = User.objects.filter(email=email)

    if filter_user_by_email.exists():
        if provider = filter_user_by_email[0].provider:

    else:
        user = {
            "email": email,
            "password" : "mypassword"
        }

        user = user.objects.create_user(user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()
