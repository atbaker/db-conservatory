from django.conf import settings

import requests

def get_all_containers():
    r = requests.get('http://%s/containers' % settings.SPIN_DOCKER_HOST)
    containers = r.json()['containers']
    return containers
