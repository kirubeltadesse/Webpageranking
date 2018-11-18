from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.environ.get('DEBUG', True) == 'True'
DEBUG = True
# Needed by django debug toolbar
INTERNAL_IPS = '127.0.0.1'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

BOKEH_RUL = 'http://localhost:5006'
