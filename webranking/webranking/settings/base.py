# from decouple import config
import os

# Obtain your own key by typing "bokeh secret" in a terminal
# the key goes below, and in the bokehserver.service file
os.environ["BOKEH_SECRET_KEY"] = "wQGYgPXx6M5ITqI3hBFZOG7GACXlUBFsWZ6J9pAfZX8X"
os.environ["BOKEH_SIGN_SESSIONS"] = "True"


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES_DIR = os.path.join(os.path.split(BASE_DIR)[0],'template')
STATIC_DIR = os.path.join(BASE_DIR,'static')

# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_9ujpl0961y(4v0hlo5hv3+-eokfty8pd&euxb!8hv82s9@$lm'

# need to be add
# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'bokeh_app.apps.BokehAppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # 'bokeh_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webranking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webranking.wsgi.application'

# Pagination allows to control how many objects per page are returned using rest_framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [STATIC_DIR,]
