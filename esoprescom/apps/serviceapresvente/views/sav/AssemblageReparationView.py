from apps.serviceapresvente.models import AssemblageReparation
from apps.serviceapresvente.models import LivraisonClient
from apps.serviceapresvente.models import Sav_request
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from apps.serviceapresvente.forms.AssemblageReparationForm import AssemblageReparationForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required



@login_required
def index(request):
    assemblagereparation_list = AssemblageReparation.objects.all()
    paginator = Paginator(assemblagereparation_list, 8)
    page = request.GET.get('page', 1)

    try:
        assemblagereparations = paginator.page(page)
    except PageNotAnInteger:
        assemblagereparations = paginator.page(1)
    except EmptyPage:
        assemblagereparations = paginator.page(paginator.num_pages)
    except:
        assemblagereparations = paginator.page(1)

    return render(request,"servicedsi/index.html",{
    'page':'savrequest',
    'subpage':'assemblage',
    'assemblagereparation_list':assemblagereparations
    })
# Les autres fonctions comme show, create, update, delete... 

def show(request, id):
    assemblagereparation = get_object_or_404(AssemblageReparation, idassemblage=id)
    detailformUpd = AssemblageReparationForm(instance=assemblagereparation)
    return render(request, 'servicedsi/assemblage/formAssemblageDetail.html', 
                  {'assemblage': assemblagereparation,
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
    assemblagereparation = get_object_or_404(AssemblageReparation, idassemblage=id)
    
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = AssemblageReparationForm(request.POST, request.FILES, instance=assemblagereparation)
            if form.is_valid():
                data = form.save(commit=False) 
                if(data.statut == "Terminé" ):
                    print('data.statut:',data.statut)
                    try:
                        livraison, created = LivraisonClient.objects.get_or_create(
                                assamblagereparation_id = data.idassemblage,
                                )
                        if created:
                            ### Mise a jour de status dans SAV Request
                            Sav_request_instance = Sav_request.objects.get(pk=data.suivicommandesav.commandesav.savrequest.idrequest)
                            Sav_request_instance.statut = 'non Livré(e)'
                            Sav_request_instance.save()
                            data.flag = True
                            data.save()
                            messages.success(request, 'Processus Logistique')
                        else:
                            print("Row not created")    
                    except IntegrityError:
                            messages.error(request, 'Erreur d\'intégrité lors de la création du processus achat !')
                else: 
                    data.save()
                    messages.success(request, 'Assemblage Sav has been saved !')
                messages.success(request, 'Assemblage has been updated !')
                return redirect('serviceapresvente:assemblage')
            else:
                print('Formulaire invalide')
                form = AssemblageReparationForm(instance=assemblagereparation)
    else:
        print('No POST data')
        form = AssemblageReparationForm(instance=assemblagereparation)
    return render(request, 'servicedsi/assemblage/formAssemblageUpd.html', 
                   {'form': form, })

@login_required
def delete(request, id):
    suivicommandesav = get_object_or_404(LivraisonClient, idassemblage=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            suivicommandesav.delete()
            messages.success(request, 'Assemblage has been deleted !')
    return redirect('serviceapresvente:assemblage')

