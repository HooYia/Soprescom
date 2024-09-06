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

from apps.serviceapresvente.models import AssemblageReparation, LivraisonClient
from apps.serviceapresvente.models.SuiviCommandeSav import SuiviCommandeSav
from apps.serviceapresvente.models.ClotureDossier import ClotureDossier
from apps.serviceapresvente.models.Recouvrement import Recouvrement
from apps.accounts.models.Customer import Customer
from apps.serviceapresvente.models.Client_sav import Client_sav
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
from django.conf import settings
from apps.serviceapresvente.models.tasks import send_email_with_template_customer

from_email = settings.EMAIL_HOST_USER


@login_required
def index(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_losgistic) :
        return redirect('dashboard:dashboard')
    sav_requests_list = Sav_request.objects.all()
    paginator = Paginator(sav_requests_list, 5)
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
    #'savrequest':sav_requests_list
    'savrequest':savrequest
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
            # print("data:",data)
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
                        messages.info(request, 'Processus Achat !')
                        
                    else:
                        messages.info(request, 'Erreur d\'intégrité lors de la création du processus achat !')
                    return redirect('serviceapresvente:savrequest')
                else:
                    # bon_pour_accord est False
                    messages.success(request, 'Sav_request a été sauvegardée sans processus d\'achat.')
                    return redirect('serviceapresvente:savrequest')
            except Exception as e:
                # print(e)
                messages.info(request, 'Une erreur s\'est produite lors de la sauvegarde.')
                return redirect('serviceapresvente:savrequest')
        else:
            messages.info(request, 'Formulaire invalide, veuillez vérifier les champs.')
            # form = Sav_requestForm()
            return redirect('serviceapresvente:savrequest')
    else:
        print("No Post form add")
        form = Sav_requestForm()
        # customers = Customer.objects.filter(is_active=True, is_deleted=False)
        # clients = Client_sav.objects.filter(is_active=True, is_deleted=False).select_related('customer')

        # Get IDs of customers already associated with a client
        associated_customer_ids = Client_sav.objects.filter(
            is_active=True,
            is_deleted=False
        ).values_list('customer_id', flat=True).distinct()

        # Exclude customers who are already associated with a client
        customers = Customer.objects.filter(
            is_active=True,
            is_deleted=False
        ).exclude(id__in=associated_customer_ids)
        print('customer: ', customers)

        return render(request, 'servicedsi/formSavAdd.html', {'form': form, 'customers':customers})
    
    

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
                        #    print('Sav_request has been saved with bon_pour_accord!')
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
                # print('Form invalid')
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
    # Fetch associated CommandeSav
    try:
        commande_sav = fiche_dentree.sav_requests  # OneToOne relation, direct access via related_name
    except CommandeSav.DoesNotExist:
        commande_sav = None
    
    # Fetch associated SuiviCommandeSav
    try:
        suivi_commande_sav = commande_sav.commandesavs if commande_sav else None  # OneToOne relation
    except SuiviCommandeSav.DoesNotExist:
        suivi_commande_sav = None
    
    # Fetch associated AssemblageReparation
    try:
        assemblage_reparation = suivi_commande_sav.suivicommandesavs if suivi_commande_sav else None  # OneToOne relation
    except AssemblageReparation.DoesNotExist:
        assemblage_reparation = None
    
    # Fetch associated LivraisonClient
    try:
        livraison_client = assemblage_reparation.assamblagereparations if assemblage_reparation else None  # OneToOne relation
    except LivraisonClient.DoesNotExist:
        livraison_client = None

    # Fetch associated Recouvrement
    try:
        recouvrement = livraison_client.livraisonclients if livraison_client else None  # OneToOne relation
    except Recouvrement.DoesNotExist:
        recouvrement = None

    # Fetch associated Cloture
    try:
        cloture_dossier = recouvrement.recouvrements if recouvrement else None  # OneToOne relation
    except ClotureDossier.DoesNotExist:
        cloture_dossier = None
    
    current_date = date.today()

    context = {
        'fiche_dentree': fiche_dentree,
        'commande_sav': commande_sav,
        'suivi_commande_sav': suivi_commande_sav,
        'assemblage_reparation': assemblage_reparation,
        'livraison_client': livraison_client,
        'recouvrement': recouvrement,
        'cloture_dossier': cloture_dossier,
        'current_date': current_date.strftime('%d/%m/%Y'),
    }
    template = get_template('servicedsi/includes/fiche_dentree.html')
    html = template.render(context)
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="SAV_{fiche_dentree.client_sav}.pdf"'
    return response

@csrf_exempt
def create_client(request):
    if request.method == 'POST':
        try:
            user_log_id = request.POST.get('userLog')
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            telephone = request.POST.get('telephone')
            adresse = request.POST.get('adresse')
            customer = get_object_or_404(Customer, id=user_log_id)
        

            # Check if a client with the same attributes already exists
            if Client_sav.objects.filter(customer=customer).exists():
                return JsonResponse({'success': False, 'message': 'A client with the same details already exists!'})

            data = {
                'client_name': f"{nom} {prenom}",
                'telephone': telephone,
                'adresse': adresse,
                'customer': customer,
                'nom': nom,
                'prenom': prenom,
                'userLog': request.user.email,
            }

            client = Client_sav(**data)
            client.save()

            # sav client acount creation email
            template_name = 'email/user_created.html'
            context = {
                'client_name': f"{nom} {prenom}",
                'user': client,
                'username': customer.username ,
                'created_by': request.user.email
            }
            to_email = [customer.email]
            subject = _('client Created')
            
            send_email_with_template_customer.delay(subject, template_name, context, to_email, from_email)
            

            return JsonResponse({
                'success': True,
                'message': 'Client added successfully!',
                'client_id': client.idclient,
                'client_name': client.client_name
            })

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})