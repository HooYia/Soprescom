from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from apps.dashboard.forms.UserAccountForm import UserAccountForm
from apps.accounts.forms.ResetPasswordForm import ResetPasswordForm
from django.contrib import messages

@login_required
def index(request):
  user = request.user
  account_form = UserAccountForm(instance=user)
  reset_password_form = ResetPasswordForm()
  reset_password_form.user = user
  
  return render(request,"dashboard/index.html",{
    'page':'account-detail',
    'account_form':account_form,
    'reset_password_form':reset_password_form
    })
  
def save_account(request):
    user = request.user
    if request.method=="POST":
      account_form = UserAccountForm(request.POST,instance=user)
      if account_form.is_valid():
          account_form.save()
          messages.success(request,'Account updated successfully')
          return redirect('dashboard:account-detail')
      else:
          messages.success(request,'Error server')
          return redirect('dashboard:account-detail')
    else:
        account_form = UserAccountForm(instance=user)
       #addresses =  Address.objects.filter(author=user)
    return redirect('dashboard:account-detail')

def reset_account_password(request):
  user = request.user
  
  if request.method == "POST":
      reset_password_form = ResetPasswordForm(request.POST)
      reset_password_form.user  = user
      if reset_password_form.is_valid():
         #save new password
         new_password = reset_password_form.cleaned_data['new_password1']
         user.set_password(new_password)
         user.save()
         update_session_auth_hash(request, user)
         messages.success(request,'Password updated successfully')
         
         return redirect('dashboard:account-detail')
      else:
         account_form = UserAccountForm(instance=user)
         messages.success(request,'Error Updating password. Pls check the form')
         return render(request,"dashboard/index.html",{
            'page':'account-detail',
            'account_form':account_form,
            'reset_password_form':reset_password_form
         })
  return redirect('dashboard:account-detail')