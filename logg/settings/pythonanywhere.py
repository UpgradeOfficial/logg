from .base import *



DEBUG = False

ALLOWED_HOSTS = ['.pythonanywhere.com']




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'logg$default',
        'USER': 'logg',
        'PASSWORD': config("PYTHONANYWHERE_DB_PASSWORD"),
        'HOST': config('PYTHONANYWHERE_DB_HOST'),
    }
}

CARD_PAYMENT_SUCCESS_URL = "https://logg.pythonanywhere.com/swagger/"