from django.conf.urls import patterns, include, url

from django.contrib import admin

from spinner.views import DatabaseListView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', DatabaseListView.as_view(), name='home'),
    url(r'^databases/', include('spinner.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
