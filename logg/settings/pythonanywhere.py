from .base import *



DEBUG = False

ALLOWED_HOSTS = ['.pythonanywhere.com']



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'logg', # Database
        'USER': config('DB_USER'), # Owner
        'PASSWORD': config('DB_PASSWORD'), # Password when install postgres
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

