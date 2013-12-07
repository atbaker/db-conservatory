from django.conf.urls import patterns, include, url

from django.contrib import admin

from spinner.views import DatabaseList
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', DatabaseList.as_view(), name='home'),
    url(r'^users/', include('profiles.urls')),
    url(r'^databases/', include('spinner.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
