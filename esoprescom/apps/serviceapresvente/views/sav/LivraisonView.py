from apps.serviceapresvente.models import Recouvrement
from apps.serviceapresvente.models import LivraisonClient
from apps.serviceapresvente.models import Sav_request
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from apps.serviceapresvente.forms.LivraisonForm import LivraisonForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    livraison_list = LivraisonClient.objects.all()
    paginator = Paginator(livraison_list, 8)
    page = request.GET.get('page', 1)

    try:
        livraisons = paginator.page(page)
    except PageNotAnInteger:
        livraisons = paginator.page(1)
    except EmptyPage:
        livraisons = paginator.page(paginator.num_pages)
    except:
        livraisons = paginator.page(1)

    return render(request,"servicedsi/index.html",{
    'page':'savrequest',
    'subpage':'livraison',
    'livraisons':livraisons
    })
# Les autres fonctions comme show, create, update, delete... 

@login_required
def show(request, id):
    livraison = get_object_or_404(LivraisonClient, idlivraisonclient=id)
    detailformUpd = LivraisonForm(instance=livraison)
    
    return render(request, 'servicedsi/livraison/formLivraisonDetail.html', 
                  {'livraison': livraison,
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
    livraison = get_object_or_404(LivraisonClient, idlivraisonclient=id)
    
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = LivraisonForm(request.POST, request.FILES, instance=livraison)
            if form.is_valid():
                data = form.save(commit=False) 
                Sav_request_instance = Sav_request.objects.get(pk=data.assamblagereparation.suivicommandesav.commandesav.savrequest.idrequest)
                print('Sav_request_instance.recouvrement_hp:',Sav_request_instance.recouvrement_hp)
                try:
                    data.save()
                    if(data.statut == "Sav livré"):
                        recouvrement, created = Recouvrement.objects.get_or_create(
                                livraisonclient_id = data.idlivraisonclient,
                                is_devea_request = Sav_request_instance.recouvrement_hp
                                )
                        if created:
                            ### Mise a jour de status dans SAV Request
                            if Sav_request_instance.recouvrement_hp:
                                Sav_request_instance.statut = 'Dossier HP à completer'
                            else:
                                Sav_request_instance.statut = 'non payé'
                            Sav_request_instance.save()
                            data.flag = True
                            data.save()
                            messages.success(request, 'Processus Recouvrement')
                        else:
                            print("Row not created")    
                    else: 
                        messages.success(request, 'Livraison Sav has been saved !')
                except IntegrityError:
                            messages.error(request, 'Erreur d\'intégrité lors de la création du processus recouvrement !')
                return redirect('serviceapresvente:livraison')
            else:
                form = LivraisonForm(instance=livraison)
        else:
          form = LivraisonForm(instance=livraison)
    else:
        form = LivraisonForm(instance=livraison)
    return render(request, 'servicedsi/livraison/formLivraisonUpd.html', 
                   {'form': form, })

@login_required
def delete(request, id):
    suivicommandesav = get_object_or_404(LivraisonClient, idlivraisonclient=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            suivicommandesav.delete()
            messages.success(request, 'LIvraison has been deleted !')
    return redirect('serviceapresvente:livraison')

