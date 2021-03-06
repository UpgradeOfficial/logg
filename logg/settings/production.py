import os
from .base import *


DEBUG = False

ALLOWED_HOSTS = []


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'staticfiles'),
# )
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