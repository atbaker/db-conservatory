from django.conf import settings
from urlparse import urljoin

import requests

def get_all_containers():
    r = requests.get(urljoin(settings.SPIN_DOCKER_ENDPOINT, 'containers'))
    containers = r.json()
    return containers
