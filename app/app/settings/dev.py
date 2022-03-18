from app.settings.base import *
import os
from dotenv import load_dotenv

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'supertopsecretproductionkey'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'django_extensions',
]

STATICFILES_DIRS = (
    BASE_DIR.parent / 'static/',
)

MEDIA_ROOT = BASE_DIR.parent / 'static/media/'

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer',
)


load_dotenv(BASE_DIR / 'app/settings/.env')
DOMAIN_NAME = 'http://127.0.0.1:8000'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True if os.getenv('EMAIL_USE_SSL') == 'True' else False