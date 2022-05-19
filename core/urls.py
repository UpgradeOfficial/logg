from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
   
    # YOUR PATTERNS For API Documentation 
    path('phone-code/', views.PhoneCode.as_view(), name='phone_code'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact_us'),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
]