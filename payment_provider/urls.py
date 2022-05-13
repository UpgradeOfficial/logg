from django.urls import path
from . import views
app_name = "payment_provider"
urlpatterns = [
    # YOUR PATTERNS For API Documentation 
    path('', views.PaymentView.as_view(), name='pay'),
    path('verify/', views.PaymentVerificationView.as_view(), name='verify_payment'),
]