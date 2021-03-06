from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from braces.views import LoginRequiredMixin

from .models import Database, Container
import spindocker

@login_required
def create_container(request, database):
    db = get_object_or_404(Database, image=database)    
    if request.user.is_authenticated():
        container = db.create_container(user=request.user)
    else:
        container = db.create_container(session_key=request.session.session_key)
        request.session.modified = True
    return HttpResponseRedirect(container.get_absolute_url())

@login_required
def update_container(request, container_id, action):
    container = get_object_or_404(Container, container_id=container_id)

    if action == 'start':
        container.start()
        return HttpResponseRedirect(container.get_absolute_url())
    elif action == 'stop':
        container.stop()
        messages.info(request, "Your database <strong>%s</strong> is now stopped. You can start it again at any time." % container.name)
    elif action == 'delete':
        container.delete()
        messages.info(request, "Your database <strong>%s</strong> was deleted." % container.name)

    return HttpResponseRedirect(reverse('container_list'))

class DatabaseList(ListView):
    model = Database

    def get_queryset(self):
        queryset = super(DatabaseList, self).get_queryset()
        queryset = queryset.filter(active=True, category='BS').order_by('order')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DatabaseList, self).get_context_data(**kwargs)
        context['datasets'] = Database.objects.filter(active=True, category='DS').order_by('order')
        return context    

class ContainerDetail(LoginRequiredMixin, DetailView):
    model = Container
    pk_url_kwarg = 'container_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_running():
            messages.info(request, "Your database <strong>%s</strong> isn't running right now. Start it below to connect to it again." % self.object.name)
            return HttpResponseRedirect(reverse('container_list'))
        else:
            return super(ContainerDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContainerDetail, self).get_context_data(**kwargs)
        context['current_info'] = self.object.get_spin_docker_info()
        return context

class ContainerList(LoginRequiredMixin, ListView):
    model = Container

    def get_queryset(self):
        queryset = super(ContainerList, self).get_queryset()
        queryset = queryset.filter(active=True, user=self.request.user).order_by('-created')
        return queryset
