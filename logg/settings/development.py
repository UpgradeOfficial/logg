from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True




DEBUG = True

INSTALLED_APPS += [
    
]

CORS_ALLOWED_ORIGINS +=[
    "http://localhost:300"

]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
