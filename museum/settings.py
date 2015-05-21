"""
Django settings for museum project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'thya4$y4yt5*%0rrlh20e29b)_d3slmef=tt#1t!h(6v(#zry)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'museum/templates/'),


)
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp',
    'bootstrap3',
    'bootstrap3_datetime',
    'wkhtmltopdf',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'museum.urls'

WSGI_APPLICATION = 'museum.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    ('css', os.path.join(BASE_DIR, 'museum/static/css/')),
    ('font-awesome', os.path.join(BASE_DIR, 'museum/static/font-awesome/')),
    ('img', os.path.join(BASE_DIR, 'museum/static/img/')),
    ('fonts', os.path.join(BASE_DIR, 'museum/static/fonts/')),
    ('js', os.path.join(BASE_DIR, 'museum/static/js/')),
    ('bootstrap3_datetime', os.path.join(BASE_DIR, 'museum/static/bootstrap3_datetime/')),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'museum/static/')
WKHTMLTOPDF_CMD_OPTIONS = {'disable-javascript': True}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'museum/media/')
