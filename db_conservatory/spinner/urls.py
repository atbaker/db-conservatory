from django.conf.urls import patterns, url
from .views import ContainerDetail, ContainerList

urlpatterns = patterns('spinner.views',
    url(r'^(?P<database>\w+)/create$', 'create_container', name='create'),    
    url(r'^(?P<container_id>\w+)$', ContainerDetail.as_view(), name='container'),
    url(r'^my-databases$', ContainerList.as_view(), name='container_list'),
)
