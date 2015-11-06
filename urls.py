from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'login/$', seconduser_login, name='seconduser_login'),
    url(r'logout/$', seconduser_logout, name='seconduser_logout'),
    url(r'register/$', seconduser_register, name='seconduser_register'),
    url(r'$', index, name='index'),
)
