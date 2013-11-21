from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'db_conservatory.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^databases/', include('spinner.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
