from django.contrib.auth.admin import UserAdmin, UserChangeForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


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




class SecondUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    username = forms.CharField(required=False)
    humancheck = forms.CharField(required=False, error_messages={'invalid':"You are not Human!"})

    class Meta:
        model = SecondUser
        fields = ('email', 'password1', 'password2')

    def clean_humancheck(self):
      if self.cleaned_data['humancheck'] != "Human":
        raise ValidationError(self.fields['humancheck'].error_messages['invalid'])
      return self

    def save(self,commit = True):
        user = super(SecondUserRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
