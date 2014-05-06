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