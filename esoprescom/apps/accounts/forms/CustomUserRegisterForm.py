from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.accounts.models import Customer
from django import forms

class  CustomUserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  def __init__(self,*args, **kwargs):
     super(CustomUserRegisterForm,self).__init__(*args, **kwargs)
     self.fields['username'].widget.attrs["class"] = 'form-control'
     self.fields['username'].widget.attrs["placeholder"] = 'Your username '
     self.fields['email'].widget.attrs["class"] = 'form-control'
     self.fields['email'].widget.attrs["placeholder"] = 'your email '
     self.fields['password1'].widget.attrs["class"] = 'form-control'
     self.fields['password1'].widget.attrs["placeholder"] = 'password 1'
     self.fields['password2'].widget.attrs["class"] = 'form-control'
     self.fields['password2'].widget.attrs["placeholder"] = 'password 2'
     self.fields['agree_terms'].widget.attrs["class"] = 'form-check-input'

     
  class Meta:
    #model = User
    model = Customer
    fields = ('username','email','agree_terms','password1','password2')
    
  
