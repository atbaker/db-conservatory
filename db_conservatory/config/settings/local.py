# Local settings
from .base import *

PRODUCTION = False

DATABASES = {
    'default': dj_database_url.config(default='postgres://dbc:dbc@localhost:5432/dbc')
}
