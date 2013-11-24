from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Database, Container

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
    request.session.modified = True
    db = get_object_or_404(Database, slug=database)
    container = db.create_container(session_key=request.session.session_key) # use DB soon
    return HttpResponseRedirect(container.get_absolute_url())

class ContainerDetailView(DetailView):
    model = Container
    pk_url_kwarg = 'container_id'

    def get_context_data(self, **kwargs):
        context = super(ContainerDetailView, self).get_context_data(**kwargs)
        context['current_info'] = self.object.get_spin_docker_info()['container']
        return context

class ContainerListView(ListView):
    model = Container

    def get_queryset(self):
        queryset = super(ContainerListView, self).get_queryset()
        queryset = queryset.filter(session_key=self.request.session.session_key)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ContainerListView, self).get_context_data(**kwargs)
        object_list = []
        for container in context['object_list']:
            if container.is_running():
                object_list.append((container, True))
            else:
                object_list.append((container, False))
        context['object_list'] = object_list
        return context
