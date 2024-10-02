from leasing.models import Client
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from apps.leasing.forms import ClientleasingForm

@login_required
def index(request):
    clients_list = Client.objects.all()
    paginator = Paginator(clients_list, 8)
    page = request.GET.get('page', 1)

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)
    except:
        clients = paginator.page(1)

    return render(request, 'leasing/clients/client_index.html', {'clients': clients})

# Les autres fonctions comme show, create, update, delete... 
def show(request, id):
    client = get_object_or_404(Client, id=id)
    return render(request, 'leasing/clients/details.html', {'client': client})

def create(request):
    if request.method == 'POST':
        form = ClientleasingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client has been saved !')
            return redirect('leasing:client-create')
    else:
        form = ClientleasingForm()
    return render(request, 'leasing/clients/formAdd.html', {'form': form})

def update(request, id):
    client = get_object_or_404(Client, idclientleasing=id)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = ClientleasingForm(request.POST, request.FILES, instance=client)
            if form.is_valid():
                form.save()
                messages.success(request, 'Client has been updated !')
                return redirect('leasing:client-update')
        else:
            form = ClientleasingForm(instance=client)
    else:
        form = ClientleasingForm(instance=client)
    return render(request, 'leasing/clients/formUpd.html', {'form': form, 'client': client})

"""
def delete(request, id):
    client = get_object_or_404(Client, idclientleasing=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            client.delete()
            messages.success(request, 'Client has been deleted !')
    return redirect('client_index')

"""