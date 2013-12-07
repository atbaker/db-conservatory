from django.conf.urls import patterns, url
from .views import UserLogin, UserCreate

urlpatterns = patterns('profiles.views',
    url(r'^login$', UserLogin.as_view(), name='login'),
    url(r'^register$', UserCreate.as_view(), name='register'),
)
