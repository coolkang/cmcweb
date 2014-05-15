import os
from cmcprj.settings.base import *


DEBUG= False


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cmcweb',
        'USER': 'root',
        'PASSWORD': 'nimd@123!',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

ALLOWED_HOSTS = [
    '128.199.236.238',
]

STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "STATIC"),
)

STATIC_ROOT = '/var/www/hadiye.org/static/'

# Used by Celery app for a message queue.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmcprj.settings.production')

# Mail Setup.




