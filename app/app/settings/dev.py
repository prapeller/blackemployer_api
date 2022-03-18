from app.settings.base import *
import os
from dotenv import load_dotenv

load_dotenv(BASE_DIR / 'app/settings/.env')

DEBUG = True
ALLOWED_HOSTS = ['*']

SECRET_KEY = 'dev_key'

DOMAIN_NAME = 'http://127.0.0.1:8000'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True if os.getenv('EMAIL_USE_SSL') == 'True' else False

MEDIA_ROOT = BASE_DIR / 'static/media/'

INSTALLED_APPS += [
    'django_extensions',
]

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer',
)


