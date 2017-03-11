import os
from .common import *

DEBUG = False

ALLOWED_HOSTS = ['*']


STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    'default': {
         'ENGINE': 'django.contrib.gis.db.backends.postgis',
         'NAME': 'comiety',
         'USER': 'comiety',
         'HOST': 'localhost',
         'PASSWORD': 'ehdwlq123',
    },
}
