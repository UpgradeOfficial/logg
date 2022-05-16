from django.urls import path
from . import views


urlpatterns = [
   
    # YOUR PATTERNS For API Documentation 
    path('phone-code/', views.PhoneCode.as_view(), name='phone-code'),
]