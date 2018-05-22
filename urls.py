from django.urls import path
from .views import *

urlpatterns = [
    path('login/', seconduser_login, name='seconduser_login'),
    path('logout/', seconduser_logout, name='seconduser_logout'),
    path('register/', seconduser_register, name='seconduser_register'),
    path('', index, name='index'),
]
