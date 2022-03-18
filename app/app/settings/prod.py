from app.settings.base import *
import os
from dotenv import load_dotenv

DEBUG = False

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

STATIC_ROOT = '/vol/web/static/'
MEDIA_ROOT = '/vol/web/static/media'

CSRF_TRUSTED_ORIGINS = ["https://blackemployer.com", "https://www.blackemployer.com"]

load_dotenv(BASE_DIR / 'app/settings/.env')
DOMAIN_NAME = "https://blackemployer.com"
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True if os.getenv('EMAIL_USE_SSL') == 'True' else False