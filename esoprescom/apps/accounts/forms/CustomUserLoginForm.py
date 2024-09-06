from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from apps.accounts.models import Customer
from django import forms

class  CustomUserLoginForm(AuthenticationForm):

  def __init__(self,*args, **kwargs):
     super(CustomUserLoginForm,self).__init__(*args, **kwargs)
     self.fields['username'].widget.attrs["class"] = 'form-control'
     self.fields['username'].widget.attrs["placeholder"] = 'Your username '
     self.fields['password'].widget.attrs["class"] = 'form-control'
     self.fields['password'].widget.attrs["placeholder"] = 'Your password '
    