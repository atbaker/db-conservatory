from django.conf.urls import patterns, url

urlpatterns = patterns('manager.views',
    url(r'^$', 'show_containers', name='show'),
    url(r'^create/$', 'create_container', name='create'),
)