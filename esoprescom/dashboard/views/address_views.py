from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.models.Address import Address
from dashboard.forms.AddressForm import AddressForm
from django.contrib import messages


@login_required
def address(request):
  user = request.user
  if request.method == 'POST':
    address_form = AddressForm(request.POST)
    if address_form.is_valid():
      address = address_form.save(commit=False) 
      address.author = user
      address.save()
      messages.success(request,'Address added successfully')
      return redirect('dashboard:address')

  else:
    address_form = AddressForm()
  addresses =  Address.objects.filter(author=user)

  return render(request,"dashboard/index.html",{
    'page':'address',
    'addresses':addresses,
    'address_form':address_form
    })

@login_required
def edit_address(request,id):
  user = request.user
  address = get_object_or_404(Address,id=id,author=user)
  if request.method == 'POST':
    if request.POST.get('_method') =='PUT':
       address_form = AddressForm(request.POST,instance=address)
       if address_form.is_valid():
         #address = address_form.save(commit=False) 
         #address.author = user
         address.save()
         messages.success(request,'Address updated successfully')
         return redirect('dashboard:address')
       else:
         return redirect('dashboard:address')
    else:
        messages.success(request,'Server error.') 
          

  else:
    address_form = AddressForm(instance=address)
  
  
  #print('addresses:',addresses)
 
  return render(request,"dashboard/index.html",{
    'page':'address',
    
    'edit_address_form':address_form
    })

def remove_address(request,id):
  user = request.user
  address = get_object_or_404(Address,id=id,author=user)
  if request.method == 'POST':
    if request.POST.get('_method') =='DELETE':
       address.delete()
       messages.success(request,'Address deleted successfully')
  
  return redirect('dashboard:address')