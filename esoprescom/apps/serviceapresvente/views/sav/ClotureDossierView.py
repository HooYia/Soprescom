from apps.serviceapresvente.models import ClotureDossier
from apps.serviceapresvente.models import Sav_request
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    cloture_list = ClotureDossier.objects.all()
    paginator = Paginator(cloture_list, 8)
    page = request.GET.get('page', 1)

    try:
        cloture_list = paginator.page(page)
    except PageNotAnInteger:
        cloture_list = paginator.page(1)
    except EmptyPage:
        cloture_list = paginator.page(paginator.num_pages)
    except:
        cloture_list = paginator.page(1)

    return render(request,"servicedsi/index.html",{
    'page':'savrequest',
    'subpage':'cloturedossier',
    'cloture_list':cloture_list
    })
# Les autres fonctions comme show, create, update, delete... 

"""
def show(request, id):
    recouvrement = get_object_or_404(RecouvrementDevea, iddevearecouvrement=id)
    detailformUpd = RecouvrementDeveaForm(instance=recouvrement)
    return render(request, 'servicedsi/devea/formRecouvrementDetail.html', 
                  {'recouvrement': recouvrement,
                   'detailformUpd':detailformUpd
                   })


def create(request):
    if request.method == 'POST':
        form = RecouvrementDeveaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Devea Order has been saved !')
            return redirect('serviceapresvente:devea')
    else:
        form = SuiviCommandeSavForm()
    return render(request, 'serviceapresvente/devea/suivicommandesav_new.html', {'form': form})


def update(request, id):
    recouvrement = get_object_or_404(RecouvrementDeva, iddevearecouvrement=id)
    
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = RecouvrementDeveaForm(request.POST, request.FILES, instance=recouvrement)
            if form.is_valid():
                data = form.save(commit=False) 
                if(data.statut == "payé" ):
                    try:
                        cloture, created = ClotureDossier.objects.get_or_create(
                                 recouvrement_ID = 'dataDevea',
                                 recouvrement_Type = 'dataDevea',
                                 Numero_Dossier = 'dataDevea',
                                 Client = 'dataDevea',
                                )
                        if created:
                            #### Mise a jour de status dans SAV Request
                            #Sav_request_instance = Sav_request.objects.get(pk=data.assamblagereparation.suivicommandesav.commandesav.savrequest.idrequest)
                            #Sav_request_instance.statut = 'non payé'
                            #Sav_request_instance.save()
                            data.flag = True
                            data.save()
                            messages.success(request, 'Processus Compta')
                        else:
                            print("Row not created")    
                    except IntegrityError:
                            messages.error(request, 'Erreur d\'intégrité lors de la création du processus achat !')
                else: 
                    data.save()
                    messages.success(request, 'Livraison Sav has been saved !')
                messages.success(request, 'Livraison has been updated !')
                return redirect('serviceapresvente:devea')
            else:
                form = RecouvrementForm(instance=recouvrement)
    else:
        form = RecouvrementForm(instance=recouvrement)
    return render(request, 'servicedsi/devea/formRecouvrementUpd.html', 
                   {'form': form, })

def delete(request, id):
    suivicommandesav = get_object_or_404(LivraisonClient, iddevearecouvrement=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            suivicommandesav.delete()
            messages.success(request, 'LIvraison has been deleted !')
    return redirect('serviceapresvente:recouvrement')
"""
