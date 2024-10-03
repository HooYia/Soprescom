from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.leasing.models import Clientleasing
from django.contrib import messages
from apps.leasing.forms import ClientleasingForm, ListeimprimanteForm, DeploiementForm, \
                               ConsommableForm, ExploitationForm


@login_required
def index(request):
    leasingClient_list = Clientleasing.objects.all()
    paginator = Paginator(leasingClient_list, 8)
    page = request.GET.get('page', 1)
    
    try:
        leasingClient_lists = paginator.page(page)
    except PageNotAnInteger:
        leasingClient_lists = paginator.page(1)
    except EmptyPage:
        leasingClient_lists = paginator.page(paginator.num_pages)
    except:
        leasingClient_lists = paginator.page(1)
    return render(request,"servicedsi/index.html",{
    'page':'leasing',
    'subpage':'clientleasing',
    'leasingClient_lists':leasingClient_lists
    })


# Les autres fonctions comme show, create, update, delete... 

def show(request, id):
    sav_request = get_object_or_404(Clientleasing, idclientleasing=id)
    form_detail = ClientleasingForm(sav_request)
    return render(request, 'servicedsi/leasing/client/details.html', {'row': form_detail,
                                                                      'modal_header':'Détails Client Leasing'})


def create(request):
    if request.method == 'POST':
        form = ClientleasingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client has been saved !')
            return redirect('leasing:Client')
    else:
        form = ClientleasingForm()
    return render(request, 'servicedsi/leasing/client/formAdd.html', {'form': form})

def update(request, id):
    get_one_Client = get_object_or_404(Clientleasing, idclientleasing=id)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = ClientleasingForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Client has been updated !')
                return redirect('leasing:client')
        else:
            form = ClientleasingForm(instance=get_one_Client)
    else:
        form = ClientleasingForm(instance=get_one_Client)
    return render(request, 'servicedsi/leasing/client/formUpd.html', {'form': form,
                                                                      'get_one_Client': get_one_Client})
"""
def delete(request, id):
    leasinglisteimprimante = get_object_or_404(LeasingListeimprimante, idclientleasing=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            leasinglisteimprimante.delete()
            messages.success(request, 'LeasingListeimprimante has been deleted !')
    return redirect('leasinglisteimprimante_index')


"""