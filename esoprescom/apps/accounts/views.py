from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from apps.accounts.forms.CustomUserRegisterForm import CustomUserRegisterForm
from apps.accounts.forms.CustomUserLoginForm import CustomUserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def sign_in(request):
  if request.user.is_authenticated:
    messages.success(request,'You are already logged in')
    return redirect('shop:home')
  form = CustomUserLoginForm()
  if request.method == "POST":
    form = CustomUserLoginForm(data=request.POST)
    if form.is_valid():
       username = form.cleaned_data['username']
       password = form.cleaned_data['password']

       user = authenticate(request,username=username,password=password)
       if user is not None:
         login(request,user)
         messages.success(request,'You are successfully logged in')
         return redirect('dashboard:dashboard')
       else:
         messages.error(request,'Incorrect username or password')
         
    else:
      messages.error(request,'Please correct the erros in the form')
  else:    
      form = CustomUserLoginForm()
      #return render(request,'accounts/signin.html',{'form':form})
  return render(request,'accounts/signin.html',{'form':form})

def sign_up(request):
  form = CustomUserRegisterForm()
  if request.method == "POST":
    form = CustomUserRegisterForm(request.POST)
    if form.is_valid():
       form.save()
       messages.success(request,'You are successfully registered')
       return redirect('accounts:sign_in')

  else:
    form = CustomUserRegisterForm()
    return render(request,'accounts/signup.html',{'form':form})
  
  return render(request,'accounts/signup.html',{'form':form})

@login_required
def logout_user(request):
  if request.user.is_authenticated:
    logout(request)
  return redirect('shop:home')


def homeviewapi(request):
    return render(request, 'index.html')

########## Update profile 
from apps.accounts.forms.ProfileForm import ProfileForm

@login_required
def update_profile(request):
    if request.method == 'POST':
        print('Request.user.profile:',request.user.profile)
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"{request.user.profile} updated!!!")
            return redirect('shop:home')
        else:
           messages.info(request, 'Updated form Invalid!')
           form = ProfileForm(instance=request.user.profile) 
    else:
        #messages.info(request, 'Error Updated !')
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/update_profile.html', {'form': form})
