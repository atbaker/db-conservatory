from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

import requests

def show_containers(req):
    r = requests.get('http://%s/containers' % settings.SPIN_DOCKER_HOST)
    return HttpResponse(r)

def create_container(req):
    r = requests.post('http://%s/containers' % settings.SPIN_DOCKER_HOST)
    return HttpResponse(r)
