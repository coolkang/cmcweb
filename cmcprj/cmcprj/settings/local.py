from cmcprj.settings.base import *


DEBUG= True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cmcweb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "STATIC"),
)


# Used by Celery app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmcprj.settings.local')