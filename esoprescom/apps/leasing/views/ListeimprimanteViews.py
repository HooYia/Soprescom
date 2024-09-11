from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.leasing.models import Listeimprimante
from apps.leasing.forms import  ListeimprimanteForm
                               
from django.contrib import messages

#@login_required
def index(request):
    imprimante_list = Listeimprimante.objects.all()
    paginator = Paginator(imprimante_list, 8)
    page = request.GET.get('page', 1)
    
    try:
        imprimante_lists = paginator.page(page)
    except PageNotAnInteger:
        imprimante_lists = paginator.page(1)
    except EmptyPage:
        imprimante_lists = paginator.page(paginator.num_pages)
    except:
        imprimante_lists = paginator.page(1)
    return render(request,"servicedsi/index.html",{
    'page':'leasing',
    'subpage':'listeimprimante',
    'imprimante_lists':imprimante_lists
    })


# Les autres fonctions comme show, create, update, delete... 

def show(request, id):
    get_listimprimante_obj = get_object_or_404(Listeimprimante, idlisteimprimante=id)
    form_detail = ListeimprimanteForm(instance=get_listimprimante_obj)
    return render(request, 'servicedsi/leasing/listeimprimante/details.html', {'form_detail': form_detail})


def create(request):
    if request.method == 'POST':
        form = ListeimprimanteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listeimprimante has been saved !')
            return redirect('leasing:imp-list')
    else:
        form = ListeimprimanteForm()
    return render(request, 'servicedsi/leasing/listeimprimante/formAdd.html', {'form': form})

def update(request, id):
    get_listimprimante_obj = get_object_or_404(Listeimprimante, idlisteimprimante=id)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = ListeimprimanteForm(request.POST, request.FILES, instance=get_listimprimante_obj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Listeimprimante has been updated !')
                return redirect('leasing:imp-list')
        else:
            form = ListeimprimanteForm(instance=get_listimprimante_obj)
    else:
        form = ListeimprimanteForm(instance=get_listimprimante_obj)
    return render(request, 'servicedsi/leasing/listeimprimante/formUpd.html', {'form': form})

"""
def delete(request, id):
    leasinglisteimprimante = get_object_or_404(idlisteimprimante, idlisteimprimante=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            leasinglisteimprimante.delete()
            messages.success(request, 'LeasingListeimprimante has been deleted !')
    return redirect('leasinglisteimprimante_index')


"""