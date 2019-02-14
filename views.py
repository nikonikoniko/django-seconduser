from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from fn.func import curried

from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View

from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView

from .models import *
from .forms import *


@curried
def seconduser_login(request):
  if request.user.is_authenticated:
      return HttpResponseRedirect(reverse('seconduser_home'))
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    redirect = request.POST['redirect']
    user = authenticate(email=email, password=password)
    if user is not None and user.email_confirmed == True:
      login(request, user)
      if redirect != "":
        return HttpResponseRedirect(redirect)
      else:
        return HttpResponseRedirect(reverse('seconduser_home'))
    else:
      return HttpResponseRedirect(reverse('seconduser_login'))
  else:
    pass
  try:
    redirect = request.GET["next"]
  except:
    redirect = ""
  return render(request, 'seconduser/login.html', {"redirect":redirect,})

@curried
def seconduser_register(modelform, request):
  print(modelform)
  if request.method == 'POST':
    form = modelform(request.POST)
    if form.is_valid():
      new_user = form.save(commit=False)
      new_user.is_active = False
      new_user.save()
      current_site = get_current_site(request)
      subject = render_to_string('seconduser/account_activation_email_subject.txt', {}).rstrip()
      message = render_to_string('seconduser/account_activation_email.html', {
        'user': new_user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)).decode('utf-8'),
        'token': account_activation_token.make_token(new_user),
      })
      new_user.email_user(subject, message)
      return render(request, 'seconduser/activation_sent.html', {})
    else:
      print("dhoiawhdoiwahdiwahdhdwa")
      print(form.errors.as_json())
      return render(request, 'seconduser/register.html', {"form":form})

  form = modelform()
  return render(request, 'seconduser/register.html', {"form":form})

class seconduser_activate(View):
    def __init__(self, usermodel):
        self.usermodel=usermodel

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = self.usermodel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, self.usermodel.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.email_confirmed = True
            user.save()
            login(request, user, backend='django_seconduser.backends.SecondUserAuth')
            return HttpResponseRedirect('/')
        else:
            # invalid link
            return render(request, 'seconduser/invalid.html')

@login_required
def seconduser_logout(request):
  logout(request)
  return HttpResponseRedirect(reverse('seconduser_login'))






class SecondUserPasswordResetView(PasswordResetView):
    form_class = SecondUserPasswordResetForm
    template_name = 'seconduser/password_reset_form.html'
    email_template_name = 'seconduser/password_reset_email.html'
    subject_template_name = 'seconduser/password_reset_subject.txt'

class SecondUserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'seconduser/password_reset_done.html'

class SecondUserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'seconduser/password_reset_complete.html'

class SecondUserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'seconduser/password_reset_confirm.html'

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = SecondUser._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, SecondUser.DoesNotExist, ValidationError):
            user = None
        return user
