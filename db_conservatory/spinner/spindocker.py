from django.conf import settings
from urlparse import urljoin

import requests
from requests.exceptions import RequestException

import logging

endpoint = settings.SPIN_DOCKER_ENDPOINT
auth = (settings.SPIN_DOCKER_USERNAME, settings.SPIN_DOCKER_PASSWORD)

logger = logging.getLogger(__name__)

def make_request(method, resource, data=None):
    url = urljoin(endpoint, resource)
    
    try:
        if method == 'GET':
            r = requests.get(url,
                auth=auth,
                )
        elif method == 'POST':
            r = requests.post(url,
                auth=auth,
                data=data)
        elif method == 'PATCH':
            r = requests.patch(url,
                auth=auth,
                data=data)
        elif method == 'DELETE':
            r = requests.delete(url,
                auth=auth)
    except RequestException:
        logger.error('Spin-docker error at resource: %s' % resource)
        return None
    
    try:
        response = r.json()
    except ValueError:
        logger.error('Spin-docker returned invalid JSON: %s %s %s' % (resource, r.status_code, r.text))
        return None
    
    return response

def get(resource):
    return make_request('GET', resource)

def post(resource, data):
    return make_request('POST', resource, data)

def patch(resource, data):
    return make_request('PATCH', resource, data)

def delete(resource):
    return make_request('DELETE', resource)
