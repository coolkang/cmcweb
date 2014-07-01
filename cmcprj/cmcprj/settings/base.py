"""
Django settings for cmcprj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True  # Moved to context based settings 


TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'analytical', # Google Analytical
    'webpages',
    'relation',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cmcprj.urls'

WSGI_APPLICATION = 'cmcprj.wsgi.application'




# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


# Additional Settings for this project
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRATION_TIME = 1800 # 30 min

# GeoIP Settings
GEOIP_PATH = os.path.join(BASE_DIR, 'GEODB')

import geoip2.database
georeader = geoip2.database.Reader(os.path.join(GEOIP_PATH,'GeoLite2-City.mmdb'))

# properties for each language
CONFIGS_DIR = os.path.join(BASE_DIR, 'CONFIGS')

# website email
INFO_EMAIL = 'hadiye.info@gmail.com'

# Google Analytics ID
#GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-52451035-1'





