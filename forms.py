from django.contrib.auth.admin import UserAdmin, UserChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import PasswordResetForm

from people.models import Person
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.conf import settings



class SecondUserChangeForm(forms.ModelForm):
  password = ReadOnlyPasswordHashField()
  issues_purchased = forms.CharField()

  class Meta:
      model = SecondUser
      fields = ("issues_purchased",)

  def clean_password(self):
      # always return the initial value
      return self.initial['password']


class SecondUserAddForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = SecondUser
        fields = ("email",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError("Password mismatch")
        return password2

    def save(self, commit=True):
        user = super(SecondUserAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SecondUserActivationEmailForm(forms.Form):
    email = forms.CharField(
        required = True,
        error_messages={'unique': 'User with this email already exists'}
    )

    class Meta:
        fields = ('email')


class SecondUserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        required = True,
        error_messages={
            'invalid': 'Username must contain only letters and numbers. Username must not contain spaces or other characters.',
            'unique': 'User with this username already exists.'
        }
    )
    email = forms.CharField(
        required = True,
        error_messages={'unique': 'User with this email already exists'}
    )

    class Meta:
        model = SecondUser
        fields = ('email', 'password1', 'password2')

    def save(self,commit = True):
        user = super(SecondUserRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user



class SecondUserPasswordResetForm(PasswordResetForm):

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = SecondUser._default_manager.filter(**{
            '%s__iexact' % SecondUser.get_email_field_name(): email,
            'email_confirmed': True,
        })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, settings.EMAIL_SENDER,
                email, html_email_template_name=html_email_template_name,
)
