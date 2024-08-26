import pdfkit
from django.http import HttpResponse
from datetime import date
from apps.serviceapresvente.models import Sav_request
from apps.serviceapresvente.models import CommandeSav
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from apps.serviceapresvente.forms.Sav_requestForm import Sav_requestForm
from apps.serviceapresvente.forms.Sav_requestUpdForm import Sav_requestUpdForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template


@login_required
def index(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    sav_requests_list = Sav_request.objects.all()
    paginator = Paginator(sav_requests_list, 8)
    page = request.GET.get('page', 1)
    #sav_requests_list = Sav_requestForm(sav_requests_list)
    try:
        savrequest = paginator.page(page)
    except PageNotAnInteger:
        savrequest = paginator.page(1)
    except EmptyPage:
        savrequest = paginator.page(paginator.num_pages)
    except:
        savrequest = paginator.page(1)
    #print('savrequest:',savrequest)
    #return render(request, 'serviceapresvente/sav_requests/sav_request_index.html', {'sav_requests': sav_requests})
    return render(request,"servicedsi/index.html",{
    'page':'savrequest',
    'subpage':'savrequest',
    'savrequest':sav_requests_list
    })


@login_required
def create_user(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        return render(request, 'servicedsi/new_user.html')
    
# Les autres fonctions comme show, create, update, delete... 
@login_required
def show(request, id):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    sav_request = get_object_or_404(Sav_request, idrequest=id)
    form_detail = Sav_requestForm(sav_request)
    return render(request, 'servicedsi/sav_details.html', {'form_detail': form_detail})

@login_required
def create(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    if request.method == 'POST':
        form = Sav_requestForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False) 
            data.userLog = request.user
            print("data:",data)
            #print('data.bon_pour_accord:',data.bon_pour_accord)
            try:
                data.save()
                if data.bon_pour_accord:
                    commandesav, created = CommandeSav.objects.get_or_create(
                        savrequest_id = data.idrequest,
                        )
                    if created:
                        data.flag = True
                        data.statut = 'pending (achat)'
                        data.save()
                        # print('Sav_request has been saved with bon_pour_accord!')
                        messages.success(request, 'Processus Achat !')
                        
                    else:
                        messages.error(request, 'Erreur d\'intégrité lors de la création du processus achat !')
                    return redirect('serviceapresvente:savrequest')
                else:
                    # bon_pour_accord est False
                    messages.success(request, 'Sav_request a été sauvegardée sans processus d\'achat.')
                    return redirect('serviceapresvente:savrequest')
            except Exception as e:
                # print(e)
                messages.error(request, 'Une erreur s\'est produite lors de la sauvegarde.')
                return render(request, 'servicedsi/formSavAdd.html', {'form': form})
        else:
            messages.error(request, 'Formulaire invalide, veuillez vérifier les champs.')
            form = Sav_requestForm()
            return render(request, 'servicedsi/formSavAdd.html', {'form': form})
    else:
        print("No Post form add")
        form = Sav_requestForm()
        return render(request, 'servicedsi/formSavAdd.html', {'form': form})
    

@login_required
def update(request, id):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    sav_request = get_object_or_404(Sav_request, idrequest=id)
    
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = Sav_requestUpdForm(request.POST, request.FILES, instance=sav_request)
            if form.is_valid():
                data = form.save(commit=False) 
                data.userLog = request.user
                try:
                    data.save()
                    if data.bon_pour_accord:
                        commandesav, created = CommandeSav.objects.get_or_create(
                            savrequest_id = data.idrequest,
                            )
                        if created:
                           data.flag = True
                           data.statut = 'pending (achat)'
                           data.save()
                           print('Sav_request has been saved with bon_pour_accord!')
                           messages.success(request, 'Processus Achat !')
                           
                        else:
                            messages.error(request, 'Erreur d\'intégrité lors de la création du processus achat !')
                        return redirect('serviceapresvente:savrequest')
                    else:
                        # bon_pour_accord est False
                        messages.success(request, 'Sav_request a été sauvegardée sans processus d\'achat.')
                        return redirect('serviceapresvente:savrequest')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Une erreur s\'est produite lors de la sauvegarde.')
                    return render(request, 'servicedsi/formSavUpd.html', {'form': form})
            else:
                print('Form invalid')
                form = Sav_requestUpdForm(instance=sav_request)
                return render(request, 'servicedsi/formSavUpd.html', {'form': form, 
                                                          'sav_request': sav_request})
        else:
            form = Sav_requestUpdForm(instance=sav_request)
            return render(request, 'servicedsi/formSavUpd.html', {'form': form, 
                                                          'sav_request': sav_request})
    else:
        form = Sav_requestUpdForm(instance=sav_request)        
        return render(request, 'servicedsi/formSavUpd.html', {'form': form, 
                                                          'sav_request': sav_request})

@login_required
def delete(request, id):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    sav_request = get_object_or_404(Sav_request, idrequest=id)
    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            sav_request.delete()
            messages.success(request, 'Sav_request has been deleted !')
    return redirect('serviceapresvente:savrequest')


@login_required
def telecharger_fiche_dentree_pdf(request, id):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic) :
        return redirect('dashboard:dashboard')
    fiche_dentree = get_object_or_404(Sav_request, idrequest=id)
    
    current_date = date.today()

    context = {
        'fiche_dentree': fiche_dentree,
       
        'current_date': current_date.strftime('%d/%m/%Y'),
    }
    template = get_template('servicedsi/includes/fiche_dentree.html')
    html = template.render(context)
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="sale_{fiche_dentree.client_sav}.pdf"'
    return response