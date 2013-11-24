# Local settings
from .base import *
import sys

PRODUCTION = False

DATABASES = {
    'default': dj_database_url.config(default='postgres://dbc:dbc@localhost:5432/dbc')
}

# Test database in sqlite3 in memory
if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
