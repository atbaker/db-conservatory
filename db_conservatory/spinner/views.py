from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import pdb
import requests

def home(req):
    data = {}
    response = requests.get('http://%s/containers' % settings.SPIN_DOCKER_HOST)
    data['running_containers'] = response.json()
    return render(req, 'base.html', data)

def show_containers(req):
    r = requests.get('http://%s/containers' % settings.SPIN_DOCKER_HOST)
    return HttpResponse(r)

def create_container(req):
    r = requests.post('http://%s/containers' % settings.SPIN_DOCKER_HOST)
    return HttpResponseRedirect(reverse('home'))
