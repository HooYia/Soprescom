from apps.serviceapresvente.models import Recouvrement
from apps.serviceapresvente.models import ClotureDossier
from apps.serviceapresvente.models import Sav_request
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from apps.serviceapresvente.forms.RecouvrementForm import RecouvrementForm
from apps.serviceapresvente.forms.RecouvrementDeveaForm import RecouvrementDeveaForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    recouvrement_list = Recouvrement.objects.all()
    paginator = Paginator(recouvrement_list, 8)
    page = request.GET.get('page', 1)

    try:
        recouvrements = paginator.page(page)
    except PageNotAnInteger:
        recouvrements = paginator.page(1)
    except EmptyPage:
        recouvrements = paginator.page(paginator.num_pages)
    except:
        recouvrements = paginator.page(1)

    return render(request,"servicedsi/index.html",{
    'page':'savrequest',
    'subpage':'recouvrement',
    'recouvrements':recouvrements
    })
# Les autres fonctions comme show, create, update, delete... 

@login_required
def show(request, id):
    recouvrement = get_object_or_404(Recouvrement, idrecouvrement=id)
    if recouvrement.is_devea_request:
        detailformUpd = RecouvrementDeveaForm(instance=recouvrement)
    else:
        detailformUpd = RecouvrementForm(instance=recouvrement)
    
    return render(request, 'servicedsi/recouvrement/formRecouvrementDetail.html', 
                  {'recouvrement': recouvrement,
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
    recouvrement = get_object_or_404(Recouvrement, idrecouvrement=id)
    
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = RecouvrementForm(request.POST, request.FILES, instance=recouvrement)
            if form.is_valid():
                data = form.save(commit=False) 
                if (data.statut == "Sav payé" or data.statut == "Dossier HP payé" ):
                    try:
                        cloturedossier, created = ClotureDossier.objects.get_or_create(
                                recouvrement_id = data.idrecouvrement,
                                )
                        if created:
                            ### Mise a jour de status dans SAV Request
                            Sav_request_instance = Sav_request.objects.get(pk=data.livraisonclient.assamblagereparation.suivicommandesav.commandesav.savrequest.idrequest)
                            Sav_request_instance.statut = 'Dossier clôturé et payé'
                            Sav_request_instance.save()
                            data.flag = True
                            data.save()
                            
                            cloturedossier.numero_dossier = Sav_request_instance.numero_dossier
                            cloturedossier.client = Sav_request_instance.client_sav.name
                            cloturedossier.resp_dossier = Sav_request_instance.resp_sav.name
                            cloturedossier.statut = Sav_request_instance.statut
                            cloturedossier.save()
                            messages.success(request, 'Processus Compta')
                        else:
                            print("Row not created")    
                    except IntegrityError:
                            messages.error(request, 'Erreur d\'intégrité lors de la création du processus achat !')
                else: 
                    data.save()
                    messages.success(request, 'Livraison Sav has been saved !')
                messages.success(request, 'Livraison has been updated !')
                return redirect('serviceapresvente:recouvrement')
            else:
                form = RecouvrementForm(instance=recouvrement)
                
    else:
        form = RecouvrementForm(instance=recouvrement)
    return render(request, 'servicedsi/recouvrement/formRecouvrementUpd.html', 
                   {'form': form, })

@login_required
def delete(request, id):
    suivicommandesav = get_object_or_404(LivraisonClient, idrecouvrement=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            suivicommandesav.delete()
            messages.success(request, 'LIvraison has been deleted !')
    return redirect('serviceapresvente:recouvrement')

