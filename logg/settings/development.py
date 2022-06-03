from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False



ALLOWED_HOSTS = [
    '*'  
]

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#INSTALLED_APPS.insert(6,"debug_toolbar") 

INSTALLED_APPS+=[]
#MIDDLEWARE.insert(3,"debug_toolbar.middleware.DebugToolbarMiddleware")
MIDDLEWARE+=[]


CORS_ALLOWED_ORIGINS +=[
    "http://localhost:3000"

]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


ROOT_URLCONF = 'logg.urls'
# INTERNAL_IPS = [

#     "127.0.0.1",
#     "localhost",
    
# ]
# DEBUG_TOOLBAR_CONFIG= {
#     "SHOW_TOOLBAR_CALLBACK": lambda request: True,
# }
# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.history.HistoryPanel',
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
#     'debug_toolbar.panels.profiling.ProfilingPanel',
# ]

import django_heroku
django_heroku.settings(locals())