from serviceapresvente.models import Instance
from serviceapresvente.models import Instance_recouvrement
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from serviceapresvente.forms.InstanceForm import InstanceForm
from serviceapresvente.forms.Instance_recouvrementForm import Instance_recouvrementForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def index(request):
    instance_list = Instance.objects.all()
    paginator = Paginator(instance_list, 8)
    page = request.GET.get('page', 1)
    
    try:
        instance_lists = paginator.page(page)
    except PageNotAnInteger:
        instance_lists = paginator.page(1)
    except EmptyPage:
        instance_lists = paginator.page(paginator.num_pages)
    except:
        instance_lists = paginator.page(1)
    
    return render(request,"servicedsi/index.html",{
    'page':'instance',
    'subpage':'instance',
    'instance_lists':instance_lists
    })
    
# Les autres fonctions comme show, create, update, delete... 
def show(request, id):
    instance = get_object_or_404(Instance, idinstance=id)
    form_instance_detail = InstanceForm(instance=instance)
    #instancerecouvrement_detail = Instance_recouvrementForm(instance)
    return render(request, 'instance/instance_detail.html',
                  {'instance':instance,
                   'form_instance_detail': form_instance_detail})

def create(request):
    if request.method == 'POST':
        form = InstanceForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False) 
            data.userLog = request.user
            print('data.is_facturable:',data.is_facturable)
            try:
                data.save()
                if data.is_facturable:
                    instance, created = Instance_recouvrement.objects.get_or_create(
                        instance_id = data.idinstance,
                        )
                    if created:
                        data.flag = True
                        data.statut = 'Non Payé'
                        data.save()
                        print('Instance has been saved')
                        messages.success(request, 'Instance has been saved')
                        return redirect('serviceapresvente:instance')
                    else:
                        messages.error(request, 'Erreur d\'intégrité lors de la création du processus achat !')
                        return redirect('serviceapresvente:instance')
                else:
                  messages.success(request, 'Instance has been saved')
                  return redirect('serviceapresvente:instance')      
            except Exception as e:
                print(e)
                return redirect('serviceapresvente:instance')
        else:
            print('fom invalid')
            print(form)
            messages.error(request, 'Formulaire invalide, veuillez vérifier les champs.')
            form = InstanceForm()
            return render(request, 'servicedsi/instance/formInstanceAdd.html', {'form': form})
    else:
        print("No Post form add")
        form = InstanceForm()
        return render(request, 'servicedsi/instance/formInstanceAdd.html', {'form': form})
    

def update(request, id):
    instance = get_object_or_404(Instance, idinstance=id)
    
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = InstanceForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                data = form.save(commit=False) 
                data.userLog = request.user
                try:
                    data.save()
                    if (data.is_facturable and data.statut=='Résolu'):
                        instance, created = Instance_recouvrement.objects.get_or_create(
                        instance_id = data.idinstance,
                          )
                        if created:
                           data.flag = True
                           data.statut = 'Non Payé'
                           data.save()
                           print('Instance has been saved')
                           messages.success(request, 'Instance has been saved')
                           
                        else:
                            messages.error(request, 'Erreur d\'intégrité lors de la création du processus achat !')
                        return redirect('serviceapresvente:instance')
                    else:
                       messages.success(request, 'Instance has been saved')
                       return redirect('serviceapresvente:instance')
                except Exception as e:
                    print(e)
            else:
                print('Form invalid')
                form = InstanceForm(instance=instance)
        else:
            form = InstanceForm(instance=instance)
    else:
        form = InstanceForm(instance=instance)        
    return render(request, 'servicedsi/instance/formInstanceUpd.html', {'form': form})

def delete(request, id):
    sav_request = get_object_or_404(Sav_request, idinstance=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            sav_request.delete()
            messages.success(request, 'Sav_request has been deleted !')
    return redirect('serviceapresvente:instance-detele')

