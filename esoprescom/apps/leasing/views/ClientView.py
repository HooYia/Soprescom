from leasing.models import Client
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from leasing.forms.ClientForm import ClientForm

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
    return render(request, 'leasing/clients/client_show.html', {'client': client})

def create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client has been saved !')
            return redirect('client_index')
    else:
        form = ClientForm()
    return render(request, 'leasing/clients/client_new.html', {'form': form})

def update(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = ClientForm(request.POST, request.FILES, instance=client)
            if form.is_valid():
                form.save()
                messages.success(request, 'Client has been updated !')
                return redirect('client_index')
        else:
            form = ClientForm(instance=client)
    else:
        form = ClientForm(instance=client)
    return render(request, 'leasing/clients/client_new.html', {'form': form, 'client': client})

def delete(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            client.delete()
            messages.success(request, 'Client has been deleted !')
    return redirect('client_index')

