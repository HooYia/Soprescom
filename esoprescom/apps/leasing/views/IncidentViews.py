from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.leasing.models import GestionIncident
from apps.leasing.forms import  GestionIncidentForm
from django.http import Http404
                               
from django.contrib import messages

#@login_required
def index(request):
    incident_list = GestionIncident.objects.all()
    paginator = Paginator(incident_list, 8)
    page = request.GET.get('page', 1)
        
    try:
        incident_lists = paginator.page(page)
    except PageNotAnInteger:
        incident_lists = paginator.page(1)
    except EmptyPage:
        incident_lists = paginator.page(paginator.num_pages)
    except:
        incident_lists = paginator.page(1)
    return render(request,"servicedsi/index.html",{
    'page':'leasing',
    'subpage':'incident',
    'incident_lists':incident_lists
    })


# Les autres fonctions comme show, create, update, delete... 

def show(request, id):
    try:
        get_incident_obj = get_object_or_404(GestionIncident, idincident=id)
    except GestionIncident.DoesNotExist:
        # Gérer l'erreur si aucun objet n'est trouvé
        raise Http404("Maintenance non trouvée")
    form_detail = GestionIncidentForm(instance=get_incident_obj)
    return render(request, 'servicedsi/leasing/incident/details.html', {'form_detail': form_detail})


def create(request):
    if request.method == 'POST':
        form = GestionIncidentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Incident has been saved !')
            return redirect('leasing:incident-list')
    else:
        form = GestionIncidentForm()
    return render(request, 'servicedsi/leasing/incident/formAdd.html', {'form': form})

def update(request, id):
    get_incident_obj = get_object_or_404(GestionIncident, idincident=id)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = GestionIncidentForm(request.POST,  instance=get_incident_obj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Incident has been updated !')
                return redirect('leasing:incident-list')
        else:
            form = GestionIncidentForm(instance=get_incident_obj)
    else:
        form = GestionIncidentForm(instance=get_incident_obj)
    return render(request, 'servicedsi/leasing/incident/formUpd.html', {'form': form})

"""
def delete(request, id):
    leasinglisteimprimante = get_object_or_404(idincident, id=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            leasinglisteimprimante.delete()
            messages.success(request, 'LeasingListeimprimante has been deleted !')
    return redirect('leasinglisteimprimante_index')


"""