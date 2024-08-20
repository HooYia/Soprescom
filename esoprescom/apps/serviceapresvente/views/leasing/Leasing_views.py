from django.shortcuts import render
from django.contrib.auth.decorators import login_required


#@login_required
def index(request):
  #user = request.user
  #addresses =  Address.objects.filter(author=user)
  return render(request,"servicedsi/index.html",{
    'page':'leasing',
    #'addresses':addresses
    })


  
         