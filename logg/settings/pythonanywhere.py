from .base import *



DEBUG = False

ALLOWED_HOSTS = ['.pythonanywhere.com']




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'logg$default',
        'USER': 'logg',
        'PASSWORD': config("PYTHONANYWHERE_DB_PASSWORD"),
        'HOST': 'logg.mysql.pythonanywhere-services.com',
    }
}