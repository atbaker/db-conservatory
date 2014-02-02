from django.conf.urls import patterns, url
from .views import ContainerDetail, ContainerList

urlpatterns = patterns('spinner.views',
    url(r'^(?P<database>\w+)/create$', 'create_container', name='create'),    
    url(r'^(?P<container_id>\w+)$', ContainerDetail.as_view(), name='container'),
    url(r'^my-databases$', ContainerList.as_view(), name='container_list'),

    # Start, stop, delete
    url(r'^(?P<container_id>\w+)/start$', 'update_container', {'action': 'start'}, name='start_container'),
    url(r'^(?P<container_id>\w+)/stop$', 'update_container', {'action': 'stop'}, name='stop_container'),
    url(r'^(?P<container_id>\w+)/delete$', 'update_container', {'action': 'delete'}, name='delete_container'),
)
