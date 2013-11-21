from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from .models import Database

import pdb
import requests

data = {}
data['PRODUCTION'] = settings.PRODUCTION

def home(req):
    data = {}
    response = requests.get('http://%s/containers' % settings.SPIN_DOCKER_HOST)
    data['running_containers'] = response.json()['containers']
    return render(req, 'index.html', data)

def create_container(request, database):
    db = get_object_or_404(Database, slug=database)
    container = db.create_container() # use DB soon
    return HttpResponseRedirect(reverse('container', kwargs={'container': container['id']}))

class ContainerView(TemplateView):
    template_name = 'container.html'
