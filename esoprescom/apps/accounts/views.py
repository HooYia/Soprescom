from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from apps.accounts.forms.CustomUserRegisterForm import CustomUserRegisterForm
from apps.accounts.forms.CustomUserLoginForm import CustomUserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.accounts.models import Customer
from apps.serviceapresvente.models.tasks import send_email_with_template_customer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.serviceapresvente.views.sav.Sav_requestView import get_random_string
from apps.serviceapresvente.models import *
from django.contrib import messages
from apps.serviceapresvente.models.tasks import send_email_with_template_customer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.accounts.models import Customer
from django.contrib.auth.hashers import make_password

from django.utils.translation import gettext as _
from django.conf import settings

from_email = settings.EMAIL_HOST_USER
from django.utils.translation import gettext as _
from django.conf import settings




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



@login_required
def users(request):
    # Fetch all customers
    customers = Customer.objects.filter(is_active=True, is_deleted=False)
    
    # Handle new customer creation
    if request.method == "POST" and 'add_customer' in request.POST:
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Additional fields based on your model
        is_staff = request.POST.get('is_staff', 'off') == 'on'
        is_compta = request.POST.get('is_compta', 'off') == 'on'
        is_logistic = request.POST.get('is_logistic', 'off') == 'on'
        is_recouvrement = request.POST.get('is_recouvrement', 'off') == 'on'
        is_instance = request.POST.get('is_instance', 'off') == 'on'
        is_leasing = request.POST.get('is_leasing', 'off') == 'on'
        is_stock = request.POST.get('is_stock', 'off') == 'on'
        is_leasing2 = request.POST.get('is_leasing2', 'off') == 'on'
        
        # Check if username or email already exists
        if Customer.objects.filter(username=username).exists():
            messages.info(request, "Username already exists!")
        elif Customer.objects.filter(email=email).exists():
            messages.info(request, "Email already exists!")
        else:
            
            #generate password
            # password = generate_password()
            new_password = get_random_string(12)
            hashed_password = make_password(new_password)
            
            # Create and save new customer
            customer = Customer(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_compta=is_compta,
                is_losgistic=is_logistic,
                is_recouvrement=is_recouvrement,
                is_instance = is_instance,
                is_leasing=is_leasing,
                is_stock=is_stock,
                password=hashed_password,
                is_leasing2=is_leasing2,
            )
            customer.save()

            template = 'email/customer_created.html'
            context = {
                'First_name': first_name,
                'Last_name': last_name,
                'username': username ,
                'mot_de_passe': new_password,
                'created_by': request.user.email,
                 'password': "new_password",
            }
            recievers = [customer.email]
            subject = _('Customer Created') , from_email
            
            send_email_with_template_customer.delay(subject, template, context, recievers, from_email) 
            
            
            messages.info(request, f"Customer added successfully!! The generated password is: {new_password}")
            return redirect('accounts:users')

    return render(request, "servicedsi/index.html", {
        'page': 'users',
        'subpage': 'users_tab',
        'customers': customers,
    })

@login_required
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == "POST":
        customer.username = request.POST['username']
        customer.email = request.POST['email']
        customer.first_name = request.POST.get('first_name', '')
        customer.last_name = request.POST.get('last_name', '')
        
        # Additional fields
        customer.is_staff = request.POST.get('is_staff', 'off') == 'on'
        customer.is_compta = request.POST.get('is_compta', 'off') == 'on'
        customer.is_losgistic = request.POST.get('is_logistic', 'off') == 'on'
        customer.is_recouvrement = request.POST.get('is_recouvrement', 'off') == 'on'
        customer.is_instance = request.POST.get('is_instance', 'off') == 'on'
        customer.is_leasing = request.POST.get('is_leasing', 'off') == 'on'
        customer.is_stock = request.POST.get('is_stock', 'off') == 'on'
        customer.is_leasing2 = request.POST.get('is_leasing2', 'off') == 'on'
        
        customer.save()
        messages.info(request, "Customer updated successfully!")
        return redirect('accounts:users')

    return render(request, "servicedsi/index.html", {
        'page': 'users',
        'subpage': 'users_tab',
        'customers': Customer.objects.all(),  # To reload the list in the background
    })

@login_required
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == "POST":
        customer.is_deleted = True
        customer.save()

        # desactivation email
        template = 'email/customer_desactivation.html'
        context = {
            'First name': customer.first_name,
            'Last name': customer.last_name,
            'username': customer.username ,
            'created_by': request.user.email
        }
        recievers = [customer.email]
        subject = _('Account deactivated')
        
        send_email_with_template_customer.delay(subject, template, context, recievers, from_email)


        messages.info(request, "Customer deleted successfully!")
        return redirect('accounts:users')

    return render(request, "servicedsi/index.html", {
        'page': 'users',
        'subpage': 'users_tab',
        'customers': Customer.objects.filter(is_active=True, is_deleted=False),  # To reload the list in the background
    })
    
    
def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser