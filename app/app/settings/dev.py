from app.settings.base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'supertopsecretproductionkey'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'django_extensions',
]

STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

MEDIA_ROOT = BASE_DIR / 'static/media'

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer')