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


from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf.urls.static import static
from core.views import custom_500_handler, Custom404, redirect_to_swagger
from user.views import MyTokenObtainPairView


urlpatterns = [
   
    # YOUR PATTERNS For API Documentation 
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # simple jwt authentication
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
   
    # Admin path
    path('admin/', admin.site.urls),
    # custom urls for core
    path('api/', include('core.urls')),
    # custom urls for users
    path('api/user/', include('user.urls', namespace='user')),
    # custom urls for payment in the future this might need to be changed
    path('api/pay/', include('payment_provider.urls')),
    # custom urls for school 
    path('api/school/', include('school.urls')),
    # custom urls for social authentication
    path('api/social-auth/', include('social_auth.urls')),
    path('', redirect_to_swagger),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
admin.site.site_header = "Logg Admin"
admin.site.site_title = "Your Admin Portal"
admin.site.index_title = "Welcome to Logg Admin Portal"

handler404 = Custom404.as_view()
handler500 = "core.views.custom_500_handler"

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]