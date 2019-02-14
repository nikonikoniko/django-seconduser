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


def registration_email(user, request):
    current_site = get_current_site(request)
    subject = render_to_string('seconduser/account_activation_email_subject.txt', {}).rstrip()
    message = render_to_string('seconduser/account_activation_email.html', {
      'user': user,
      'domain': current_site.domain,
      'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
      'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)
    return render(request, 'seconduser/activation_sent.html', {})


@curried
def seconduser_login(request):
  if request.user.is_authenticated:
      return HttpResponseRedirect(reverse('seconduser_home'))

  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    redirect = request.POST['redirect']
    user = authenticate(email=email, password=password)

    if user is None:
        msg = f"Username or password wrong"
        return render(request, 'seconduser/login.html', {"redirect":redirect, "msg": msg})

    if user.email_confirmed == True:
      login(request, user)
      if redirect != "":
        return HttpResponseRedirect(redirect)
      else:
        return HttpResponseRedirect(reverse('seconduser_home'))
    else:
        msg = f"Account is not confirmed.  <strong><a href={reverse('seconduser_resend')}>Click here to resend activation email</a></strong>"
        return render(request, 'seconduser/login.html',
            {"redirect":redirect, "msg": msg})

  try:
    redirect = request.GET["next"]
  except:
    redirect = ""
  return render(request, 'seconduser/login.html', {"redirect":redirect,})

@curried
def seconduser_register(modelform, request):
  if request.method == 'POST':
    form = modelform(request.POST)
    if form.is_valid():
      new_user = form.save(commit=False)
      new_user.is_active = False
      new_user.save()
      return registration_email(new_user, request)
    else:
      return render(request, 'seconduser/register.html', {"form":form})

  form = modelform()
  return render(request, 'seconduser/register.html', {"form":form})


class seconduser_resend_register(View):
    usermodel = SecondUser

    def get(self, request):
        if request.user.is_authenticated:
          return HttpResponseRedirect(reverse('seconduser_home'))
        form = SecondUserActivationEmailForm
        return render(request,
            'seconduser/resend_activation_email.html',
            {"form":form, "url": reverse('seconduser_resend')})

    def post(self, request):
      if request.user.is_authenticated:
          return HttpResponseRedirect(reverse('seconduser_home'))

      form = SecondUserActivationEmailForm(request.POST)

      if form.is_valid():
        f = form.cleaned_data['email']
        new_user = self.usermodel.objects.get(email=f)
        if new_user.email_confirmed == True:
          return HttpResponseRedirect(reverse('seconduser_home'))
        return registration_email(new_user, request)
      else:
        return render(request,
            'seconduser/resend_activation_email.html',
            {"form":form, "url": reverse('seconduser_resend')})




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
            return HttpResponseRedirect(reverse('seconduser_home'))
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
