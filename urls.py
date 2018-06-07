from django.urls import path
from .views import *

from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login/', seconduser_login, name='seconduser_login'),
    # path('logout/', seconduser_logout, name='seconduser_logout'),
    # path('register/', seconduser_register, name='seconduser_register'),
    # path('', index, name='index'),
    path('password_reset/', SecondUserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', SecondUserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', SecondUserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', SecondUserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
