from django.urls import path
from . import views
app_name = "payment_provider"
urlpatterns = [
    # YOUR PATTERNS For API Documentation 
    path('', views.PaymentView.as_view(), name='pay'),
    path('verify/', views.PaymentVerificationView.as_view(), name='verify_payment'),
    path('paystack_webhook/', views.PaystackWebhookView.as_view(), name='paystack_webhook'),
    path('flutterwave-webhook/', views.FlutterwaveWebhookView.as_view(), name='flutterwave_webhook'),
]