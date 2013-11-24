from django.conf.urls import patterns, url
from .views import ContainerDetailView, ContainerListView

urlpatterns = patterns('spinner.views',
    url(r'^(?P<database>\w+)/create$', 'create_container', name='create'),    
    url(r'^(?P<container_id>\w+)$', ContainerDetailView.as_view(), name='container'),
    url(r'^my-databases$', ContainerListView.as_view(), name='container_list'),
)
