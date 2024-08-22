from apps.serviceapresvente.models import SuiviCommandeSav
from apps.serviceapresvente.models import AssemblageReparation
from apps.serviceapresvente.models import Sav_request
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from apps.serviceapresvente.forms.SuiviCommandeSavForm import SuiviCommandeSavForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    suivicommandesavs_list = SuiviCommandeSav.objects.all()
    paginator = Paginator(suivicommandesavs_list, 8)
    page = request.GET.get('page', 1)

    try:
        suivicommandesavs = paginator.page(page)
    except PageNotAnInteger:
        suivicommandesavs = paginator.page(1)
    except EmptyPage:
        suivicommandesavs = paginator.page(paginator.num_pages)
    except:
        suivicommandesavs = paginator.page(1)

    return render(request,"servicedsi/index.html",{
    'page':'savrequest',
    'subpage':'suivicommandesav',
    'suivicommandesavs_list':suivicommandesavs
    })
# Les autres fonctions comme show, create, update, delete... 

@login_required
def show(request, id):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    suivicommandesav = get_object_or_404(SuiviCommandeSav, idsuivicommandesav=id)
    detailformUpd = SuiviCommandeSavForm(instance=suivicommandesav)
    return render(request, 'servicedsi/suivicommandesav/formSuivicommandeDetail.html', 
                  {'suivicommandesav': suivicommandesav,
                   'detailformUpd':detailformUpd
                   })
"""
def create(request):
    if request.method == 'POST':
        form = SuiviCommandeSavForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'SuiviCommandeSav has been saved !')
            return redirect('suivicommandesav_index')
    else:
        form = SuiviCommandeSavForm()
    return render(request, 'serviceapresvente/suivicommandesavs/suivicommandesav_new.html', {'form': form})
"""
@login_required
def update(request, id):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    suivicommandesav = get_object_or_404(SuiviCommandeSav, idsuivicommandesav=id)
    
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            #print("method Put")
            form = SuiviCommandeSavForm(request.POST, request.FILES, instance=suivicommandesav)
            if form.is_valid():
                #print("form Valid")
                #data = form.save(commit=False) 
                try:
                    data = form.save() 
                    if(data.statut == "Reçu" ):
                        #print('data.statut:',data.statut)
                        assemblage, created = AssemblageReparation.objects.get_or_create(
                                suivicommandesav_id = data.idsuivicommandesav,
                                )
                        if created:
                            ### Mise a jour de status dans SAV Request
                            Sav_request_instance = Sav_request.objects.get(pk=data.commandesav.savrequest.idrequest)
                            Sav_request_instance.statut = 'pending (DSI - Assemblage)'
                            Sav_request_instance.save()
                            data.flag = True
                            data.save()
                            messages.success(request, 'Processus DSI')
                        else:
                            print("Row not created")    
                    
                    else: 
                        messages.success(request, 'Suivi Commande Sav has been saved !')
                    
                    return redirect('serviceapresvente:suivicommandesav')
                except Exception as e:
                    print(e)
                    messages.error(request, 'SuiviCommandeSav  has not been updated !')
                    
            else:
                form = SuiviCommandeSavForm(instance=suivicommandesav)
        else:
          print('it\'s not PUT method')
          form = SuiviCommandeSavForm(instance=suivicommandesav)
    else:
        form = SuiviCommandeSavForm(instance=suivicommandesav)
    return render(request, 'servicedsi/suivicommandesav/formSuiviCommandeUpd.html', 
                   {'form': form, })
    
    
@login_required
def delete(request, id):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    suivicommandesav = get_object_or_404(SuiviCommandeSav, idsuivicommandesav=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            suivicommandesav.delete()
            messages.success(request, 'SuiviCommandeSav has been deleted !')
    return redirect('suivicommandesav_index')

