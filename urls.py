from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'login/$', member_login, name='member_login'),
    url(r'logout/$', member_logout, name='member_logout'),
    url(r'register/$', member_register, name='member_register'),
    url(r'$', index, name='index'),
)
