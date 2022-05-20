import os
from .base import *

import django_heroku


DEBUG = False
INSTALLED_APPS.insert(6, 'cloudinary_storage')
INSTALLED_APPS.insert(7, 'cloudinary')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET')
}

ALLOWED_HOSTS = ['.herokuapp.com']

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


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

django_heroku.settings(locals())