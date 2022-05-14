from django.urls import path

from .views import FacebookSocialAuthView

app_name  = "social_auth"

urlpatterns = [
    path('facebook/', FacebookSocialAuthView.as_view(), name='facebook-login'), 
]