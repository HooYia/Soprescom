from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.leasing.models import Deploiement,Listeimprimante
from apps.leasing.forms import  DeploiementForm
                               
from django.contrib import messages

@login_required
def index(request):
    deploiement_list = Deploiement.objects.all()
    paginator = Paginator(deploiement_list, 5)
    page = request.GET.get('page', 1)
    
    try:
        deploiement_lists = paginator.page(page)
    except PageNotAnInteger:
        deploiement_lists = paginator.page(1)
    except EmptyPage:
        deploiement_lists = paginator.page(paginator.num_pages)
    except:
        imprimante_lists = paginator.page(1)
    return render(request,"servicedsi/index.html",{
    'page':'leasing',
    'subpage':'deploiement',
    'deploiement_lists':deploiement_lists
    })


# Les autres fonctions comme show, create, update, delete... 

def show(request, id):
    get_deploiement_obj = get_object_or_404(Deploiement, idrequest=id)
    form_detail = DeploiementForm(instance=get_deploiement_obj)
    return render(request, 'servicedsi/leasing/liste_imprimante.html', {'form_detail': form_detail})


def create(request):
    if request.method == 'POST':
        form = DeploiementForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False) 
            try:
                deploiement_imprimante_instance = Listeimprimante.objects.get(pk=data.listeimprimante.idlisteimprimante)
                print("deploiement_imprimante_instance",deploiement_imprimante_instance)
                deploiement_imprimante_instance.flag = 1
                deploiement_imprimante_instance.save()
                form.save()
                messages.success(request, 'Deploiement has been saved !')
            except:
                messages.error(request, 'Erreur de deploiement d\'imprimante !')  
            
            return redirect('leasing:deploiement-list')
    else:
        form = DeploiementForm()
    return render(request, 'servicedsi/leasing/deploiement/formAdd.html', {'form': form})

def update(request, id):
    get_deploiement_obj = get_object_or_404(Deploiement, iddeploiement=id)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = DeploiementForm(request.POST,instance=get_deploiement_obj)
            if form.is_valid():
                data = form.save(commit=False) 
                try:
                    deploiement_imprimante_instance = Listeimprimante.objects.get(pk=data.listeimprimante.idlisteimprimante)
                    print("deploiement_imprimante_instance",deploiement_imprimante_instance)
                    deploiement_imprimante_instance.flag = 1
                    deploiement_imprimante_instance.save()
                    form.save()
                    messages.success(request, 'Deploiement has been saved !')
                except:
                    messages.error(request, 'Erreur de deploiement d\'imprimante !')  
            
                return redirect('leasing:deploiement-list')
            else:
                form = DeploiementForm(instance=get_deploiement_obj)
        else:
            form = DeploiementForm(instance=get_deploiement_obj)
    else:
        form = DeploiementForm(instance=get_deploiement_obj)
    return render(request, 'servicedsi/leasing/deploiement/formUpd.html', {'form': form})

"""
def delete(request, id):
    get_deploiement_obj = get_object_or_404(Deploiement, iddeploiement=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            get_deploiement_obj.delete()
            messages.success(request, 'Deploiement has been deleted !')
    return redirect('leasing:deploiement-list')


"""