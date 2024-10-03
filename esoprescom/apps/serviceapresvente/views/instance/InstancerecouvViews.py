from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.serviceapresvente.models import Instance
from apps.serviceapresvente.models import Instance_recouvrement
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from apps.serviceapresvente.forms.Instance_recouvrementForm import Instance_recouvrementForm
from django.db import IntegrityError

@login_required
def index(request):
    instancerevouv_list = Instance_recouvrement.objects.all()
    paginator = Paginator(instancerevouv_list, 8)
    page = request.GET.get('page', 1)
    
    try:
        instancerevouv_lists = paginator.page(page)
    except PageNotAnInteger:
        instancerevouv_lists = paginator.page(1)
    except EmptyPage:
        instancerevouv_lists = paginator.page(paginator.num_pages)
    except:
        instancerevouv_lists = paginator.page(1)
    
    return render(request,"servicedsi/index.html",{
    'page':'instance',
    'subpage':'instance_recouvrement',
    'instancerevouv_lists':instancerevouv_lists
    })
    
def show(request, id):
    instancerecouv = get_object_or_404(Instance_recouvrement, idrecouv=id)
    form_instance_detail = Instance_recouvrementForm(instance=instancerecouv)
    
    return render(request, 'servicedsi/instance_recouvrement/instancerecouv_detail.html',
                  {'instancerecouv':instancerecouv,
                   'form_instance_detail': form_instance_detail})

   

def update(request, id):
    instance = get_object_or_404(Instance_recouvrement, idrecouv=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = Instance_recouvrementForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                data = form.save(commit=False) 
                data.userLog = request.user
                try:
                    data.save()
                    if (data.facture_statut == "Payé"):
                      data.flag = True
                      data.save()
                      print('Instance recouv has been saved')
                      print('Instance recouv has been saved')
                      messages.success(request, 'Instance  has been saved')
                      return redirect('serviceapresvente:instancerecouv')     
                    else:
                       messages.success(request, 'Instance has been saved')
                       return redirect('serviceapresvente:instancerecouv')
                except Exception as e:
                    print(e)
            else:
                print('Form invalid')
                print('form:',form)
                form = Instance_recouvrementForm(instance=instance)
        else:
            form = Instance_recouvrementForm(instance=instance)
    else:
        form = Instance_recouvrementForm(instance=instance)        
    return render(request, 'servicedsi/instance_recouvrement/formInstanceUpd.html', {'form': form})

  
         