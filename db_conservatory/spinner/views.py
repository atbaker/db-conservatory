from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from braces.views import LoginRequiredMixin

from .models import Database, Container
from .utils import get

def create_container(request, database):
    db = get_object_or_404(Database, slug=database)    
    if request.user.is_authenticated():
        container = db.create_container(user=request.user)
    else:
        container = db.create_container(session_key=request.session.session_key)
        request.session.modified = True
    return HttpResponseRedirect(container.get_absolute_url())

class DatabaseList(ListView):
    model = Database

    def get_queryset(self):
        queryset = super(DatabaseList, self).get_queryset()
        queryset = queryset.filter(active=True, category='BS')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DatabaseList, self).get_context_data(**kwargs)
        context['datasets'] = Database.objects.filter(active=True, category='DS')
        context['all_containers'] = len(get('containers'))
        return context    

class ContainerDetail(DetailView):
    model = Container
    pk_url_kwarg = 'container_id'

    def get_context_data(self, **kwargs):
        context = super(ContainerDetail, self).get_context_data(**kwargs)
        context['current_info'] = self.object.get_spin_docker_info()
        return context

class ContainerList(LoginRequiredMixin, ListView):
    model = Container

    def get_queryset(self):
        queryset = super(ContainerList, self).get_queryset()
        queryset = queryset.filter(active=True, user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ContainerList, self).get_context_data(**kwargs)
        object_list = []
        for container in context['container_list']:
            if container.is_running():
                object_list.append((container, True))
            else:
                object_list.append((container, False))
        context['container_list'] = object_list
        return context
