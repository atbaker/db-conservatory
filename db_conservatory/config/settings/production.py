# Production settings
from .base import *

PRODUCTION = True

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'TIMEOUT': 1000,
        'BINARY': True,
        'OPTIONS': {
            'tcp_nodelay': True,
            'remove_failed': 4
        }
    }
}
