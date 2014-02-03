from django.conf.urls import patterns, include, url

from django.contrib import admin

from spinner.views import DatabaseList
from profiles.views import UserCreate
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', DatabaseList.as_view(), name='home'),
    # url(r'^register$', UserCreate.as_view(), name='register'),
    url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'home'}, name='logout'),
    url(r'^databases/', include('spinner.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
