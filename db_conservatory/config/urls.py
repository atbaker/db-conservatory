from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.decorators.cache import cache_page

from django.contrib import admin

from spinner.views import DatabaseList
from profiles.views import UserCreate
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', cache_page(60 * 15)(DatabaseList.as_view()), name='home'),
    url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'home'}, name='logout'),
    url(r'^databases/', include('spinner.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if not settings.PRODUCTION:
    urlpatterns += (url(r'^register$', UserCreate.as_view(), name='register'),)
