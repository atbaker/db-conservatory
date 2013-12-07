from django.conf.urls import patterns, url
from .views import UserCreate

urlpatterns = patterns('profiles.views',
    url(r'^register$', UserCreate.as_view(), name='register'),
)
