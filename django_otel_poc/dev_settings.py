from .settings import *

from .settings import configure_logging

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


LOGGING = configure_logging(['async', 'console'], '127.0.0.1:9200')


