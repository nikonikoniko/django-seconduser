from django.db import models

from django.utils.translation import ugettext_lazy as _

from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser

from .managers import *
from django.contrib.auth.models import User as AuthUser, UserManager
from django.core.mail import send_mail

from noncitizenarchive.settings import EMAIL_HOST

class SecondUser(AbstractBaseUser):
  email = models.EmailField(max_length=200, unique=True)
  email_confirmed = models.BooleanField(default=False)
  USERNAME_FIELD = 'email'
  objects = UserManager()

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def email_user(self, subject, message):
    send_mail(
        subject,
        message,
        'admin@test',
        [self.email],
        fail_silently=False,
    )
    return False

  def subscribed():
    pass
  def is_staff():
    return False

  def __unicode__(self):
    return self.email
