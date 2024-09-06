from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.leasing.models import Consommable
from apps.leasing.forms import  ConsommableForm
                               
from django.contrib import messages

#@login_required
def index(request):
    consommable_list = Consommable.objects.all()
    paginator = Paginator(consommable_list, 5)
    page = request.GET.get('page', 1)
    
    try:
        consommable_lists = paginator.page(page)
    except PageNotAnInteger:
        consommable_lists = paginator.page(1)
    except EmptyPage:
        consommable_lists = paginator.page(paginator.num_pages)
    except:
        imprimante_lists = paginator.page(1)
    return render(request,"servicedsi/index.html",{
    'page':'leasing',
    'subpage':'consommable',
    'consommable_lists':consommable_lists
    })


# Les autres fonctions comme show, create, update, delete... 

def show(request, id):
    sav_request = get_object_or_404(Consommable, id=id)
    form_detail = ConsommableForm(sav_request)
    return render(request, 'servicedsi/leasing/consommable/detail.html', {'form_detail': form_detail})


def create(request):
    if request.method == 'POST':
        form = ConsommableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consommable has been saved !')
            return redirect('leasing:consommable-list')
    else:
        form = ConsommableForm()
    return render(request, 'servicedsi/leasing/consommable/formAdd.html', {'form': form})

def update(request, id):
    get_consommable = get_object_or_404(Consommable, id=id)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = ConsommableForm(request.POST,instance=get_consommable)
            if form.is_valid():
                form.save()
                messages.success(request, 'Consommable has been updated !')
                return redirect('leasing:consommable-list')
        else:
            form = ConsommableForm(instance=get_consommable)
    else:
        form = ConsommableForm(instance=get_consommable)
    return render(request, 'servicedsi/leasing/consommable/formUpd.html', {'form': form, 'get_consommable': get_consommable})

"""
def delete(request, id):
    leasinglisteimprimante = get_object_or_404(LeasingListeimprimante, id=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            leasinglisteimprimante.delete()
            messages.success(request, 'LeasingListeimprimante has been deleted !')
    return redirect('leasinglisteimprimante_index')


"""