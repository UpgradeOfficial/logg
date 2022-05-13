"""logg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from core.views import custom_500_handler, Custom404, redirect_to_swagger


urlpatterns = [
   
    # YOUR PATTERNS For API Documentation 
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # simple jwt authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Admin path
    path('admin/', admin.site.urls),
    # custom urls
    path('api/user/', include('user.urls')),
    # custom urls for payment in the future this might need to be changed
    path('api/pay/', include('payment_provider.urls')),
    path('', redirect_to_swagger),
]

admin.site.site_header = "Logg Admin"
admin.site.site_title = "Your Admin Portal"
admin.site.index_title = "Welcome to Logg Admin Portal"

handler404 = Custom404.as_view()
handler500 = "core.views.custom_500_handler"