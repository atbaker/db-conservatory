from django.conf.urls import patterns, url
from .views import ContainerView

urlpatterns = patterns('spinner.views',
    url(r'^$', 'home', name='home'),
    url(r'^(?P<database>\w+)/create$', 'create_container', name='create'),    
    url(r'^(?P<container>\w+)$', ContainerView.as_view(), name='container'),
)