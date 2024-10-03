from django.http import Http404
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.leasing.models import Maintenance
from apps.leasing.models import Deploiement
from apps.leasing.forms import  MaintenanceForm
                               
from django.contrib import messages

@login_required
def index(request):
    #maintenance_list = Maintenance.objects.all()
    #imprimante_site_list = Deploiement.objects.all()
    # Charger toutes les maintenances avec les informations d'imprimantes et leurs déploiements associés
    maintenance_list = Maintenance.objects.select_related('imprimante', 'imprimante__deploiement').all()
    
    paginator = Paginator(maintenance_list, 8)
    page = request.GET.get('page', 1)
    
    try:
        maintenance_lists = paginator.page(page)
    except PageNotAnInteger:
        maintenance_lists = paginator.page(1)
    except EmptyPage:
        maintenance_lists = paginator.page(paginator.num_pages)
    except:
        maintenance_lists = paginator.page(1)
    
    return render(request,"servicedsi/index.html",{
    'page':'leasing',
    'subpage':'maintenance',
    'maintenance_lists':maintenance_lists,
 
    })


# Les autres fonctions comme show, create, update, delete... 
@login_required
def show(request, id):
    #get_maintenance_obj = get_object_or_404(Maintenance, idmaintenance=id)
    #get_maintenance_obj = Maintenance.objects.select_related('imprimante', 'imprimante__deploiement').filter(idmaintenance=id).first()
    # Récupérer l'objet Maintenance avec select_related
    try:
        get_maintenance_obj = Maintenance.objects.select_related('imprimante', 'imprimante__deploiement').get(idmaintenance=id)
    except Maintenance.DoesNotExist:
        # Gérer l'erreur si aucun objet n'est trouvé
        raise Http404("Maintenance non trouvée")
    form_detail = MaintenanceForm(instance=get_maintenance_obj)
    return render(request, 'servicedsi/leasing/maintenance/details.html', {'form_detail': form_detail})

@login_required
def create(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'LeasingMaintenance has been saved !')
            return redirect('leasing:maintenance-list')
    else:
        form = MaintenanceForm()
    return render(request, 'servicedsi/leasing/maintenance/formAdd.html', {'form': form})
@login_required
def update(request, id):
    get_maintenance_obj = get_object_or_404(Maintenance, idmaintenance=id)
    ## get detail
    get_imprimante_obj = Maintenance.objects.select_related('imprimante', 'imprimante__deploiement').get(idmaintenance=id)
    
    if request.POST.get('_method') == 'PUT':
        form = MaintenanceForm(request.POST,instance=get_maintenance_obj)
        if form.is_valid():
                form.save()
                messages.success(request, 'Maintenance has been updated !')
                return redirect('leasing:maintenance-list')
        else:
            form = MaintenanceForm(instance=get_maintenance_obj)
    else:
        form = MaintenanceForm(instance=get_maintenance_obj)
    #print('form:',form.instance.idmaintenance)
    
    return render(request, 'servicedsi/leasing/maintenance/formUpd.html', {'form': form,
                                                                           'get_imprimante_obj':get_imprimante_obj})

"""
def delete(request, id):
    get_maintenance_obj = get_object_or_404(idmaintenance, idmaintenance=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            get_maintenance_obj.delete()
            messages.success(request, 'LeasingMaintenance has been deleted !')
    return redirect('leasing:maintenance-list')


"""