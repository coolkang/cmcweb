from cmcprj.settings.base import *


DEBUG= True

TEMPLATE_DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+8tikx+u1!5pb=w!jg6&qd=t^x0&t4_-&v0vx82gq%2t7b8-bo'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'cmcweb.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "STATIC"),
)


# Used by Celery app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmcprj.settings.local')

# Email setup for local; it sends emails to standard output, no real email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = '' 
EMAIL_USE_TLS = False


# Logging setting
LOG_LEVEL = 20 # logging.INFO
