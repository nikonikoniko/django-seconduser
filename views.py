from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf


from .models import *
from .forms import *




@login_required
def index(request):
  user = request.user

  return render(request, 'seconduser/index.html', {"user":user,})

def seconduser_login(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    redirect = request.POST['redirect']
    user = authenticate(email=email, password=password)
    print ("aaaaaaaaaaaaaaaa")
    print (user)
    if user is not None:
      print ("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
      login(request, user)
      if redirect != "":
        return HttpResponseRedirect(redirect)
      else:
        return HttpResponseRedirect('/accounts/')
    else:
      return HttpResponseRedirect('/accounts/login/')
  else:
    pass
  try:
    redirect = request.GET["next"]
  except:
    redirect = ""
  return render(request, 'seconduser/login.html', {"redirect":redirect,})

def seconduser_register(request):
  if request.method == 'POST':
    form = SecondUserRegistrationForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      new_user = authenticate(email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password2'])
      login(request, new_user)
      return HttpResponseRedirect('/accounts/')
    else:
      return render(request, 'seconduser/register.html', {"form":form})

  form = SecondUserRegistrationForm()
  return render(request, 'seconduser/register.html', {"form":form})

@login_required
def seconduser_logout(request):
  logout(request)
  return HttpResponseRedirect('/accounts/login')
