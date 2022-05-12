import os
from .base import *

import django_heroku


DEBUG = False

ALLOWED_HOSTS = ['*']


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


django_heroku.settings(locals())