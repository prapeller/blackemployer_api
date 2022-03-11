from app.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['blackemployer.com']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qvsz6f(6dm0+$y7r+btmd&k&%!ku&4b-8k#&fb3+1nxqr!mctk'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'NAME': 'blackemployer_db',
        'PASSWORD': 'secretpass',
        'HOST': 'db',
        'PORT': '5432'
    }
}

MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static/'