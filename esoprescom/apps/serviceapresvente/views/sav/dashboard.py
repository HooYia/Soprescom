from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime,timedelta

import json
from django.http import JsonResponse
from apps.serviceapresvente.models import Sav_request,Instance,Client_sav,Personnels, \
                            Instance_recouvrement
                            
from apps.leasing.models import  Clientleasing,Listeimprimante,Deploiement, \
                                 Consommable, Exploitation
from apps.serviceapresvente.views.sav.Sav_requestView import get_random_string
from utlis.utils import generate_password
from django.db.models import Count,Sum, Case, When, Sum,F,Q  
from django.db.models import OuterRef, Subquery               
from apps.serviceapresvente.models import *
from django.core.serializers import serialize
from django.db.models import Prefetch
from django.contrib import messages
from apps.serviceapresvente.models.tasks import send_email_with_template_customer
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from django.db import transaction
from apps.accounts.models import Customer
from django.contrib.auth.hashers import make_password


from django.utils.translation import gettext as _
from django.conf import settings


from utlis.utils import generate_password


from_email = settings.EMAIL_HOST_USER


today_date = datetime.now()
date_old_days_ago = datetime.now() - timedelta(days=180)

@login_required
def dashboard(request):
    
    context = {'segment': 'index'}
    ##########
    """Dashboard page """
    diagnostique_interne = 0
    Dossier_cloture_paye = 0
    Dossier_HP=0
    pending_achat = 0
    commande_placee = 0
    pending_logistique = 0
    reception_depot_france = 0
    reception_depot_dubai = 0
    sous_douane_malienne = 0
    pending_DSI_Assemblage = 0
    termine = 0
    sav_livre = 0
    sav_non_livre = 0
    sav_paye = 0
    sav_non_paye = 0
    nbr_sav = 0
    total_requests = 0
    nbr_sav_cloture = 0
    agg_status_SAV = ''
    detail_status_sav =''
    client_agg=''
    progress = {}
    row = {}

    try:
        agg_status_SAV,detail_status_sav = Sav_request.sav_query_instance()
        agg_status_SAV = (
            Sav_request.objects
            .filter(created_at__gte=date_old_days_ago)  # Added time filter
            .values('statut')
            .annotate(status_count=Count('idrequest'))
            .union(
                CommandeSav.objects.filter(created_at__gte=date_old_days_ago).values('statut').annotate(status_count=Count('idcommandesav')),
                SuiviCommandeSav.objects.filter(created_at__gte=date_old_days_ago).values('statut').annotate(status_count=Count('idsuivicommandesav')),
                AssemblageReparation.objects.filter(created_at__gte=date_old_days_ago).values('statut').annotate(status_count=Count('idassemblage')),
                Recouvrement.objects.filter(created_at__gte=date_old_days_ago).values('statut').annotate(status_count=Count('idrecouvrement')),
                ClotureDossier.objects.filter(created_at__gte=date_old_days_ago).values('statut').annotate(status_count=Count('idcloturedossier'))
            )
        )
        client_agg = Sav_request.sav_query_client()
      
        for line in detail_status_sav:
                # Assuming line['resp_sav'] contains the `Sav_request` instance ID or some identifier related to `Sav_request`
            sav_request = Sav_request.objects.filter(created_at__gte=date_old_days_ago).select_related('client_sav').get(idrequest=line['idrequest'])
                        
            if sav_request.client_sav:  # Check if client_sav is not None
                line['resp_sav_name'] = f"{sav_request.client_sav.nom} {sav_request.client_sav.prenom}"
            else:
                line['resp_sav_name'] = "N/A"

        for line in agg_status_SAV:
            if line['statut'] == 'Diagnostique interne':
                diagnostique_interne = line['status_count']
                nbr_sav += diagnostique_interne
            elif line['statut'] == 'pending (achat)':
                pending_achat = line['status_count']
                nbr_sav += pending_achat
            elif line['statut'] == 'commande placée':
                commande_placee = line['status_count']
                nbr_sav += commande_placee
            elif line['statut'] == 'pending (logistique)':
                pending_logistique = line['status_count']
                nbr_sav += pending_logistique
            elif line['statut'] == 'Réception dépôt France':
                reception_depot_france = line['status_count']
                nbr_sav += reception_depot_france
            elif line['statut'] == 'Réception dépôt Dubaï':
                reception_depot_dubai = line['status_count']
                nbr_sav += reception_depot_dubai
            elif line['statut'] == 'Sous Douane Malienne':
                sous_douane_malienne = line['status_count']
                nbr_sav += sous_douane_malienne
            elif line['statut'] == 'pending (DSI - Assemblage)':
                pending_DSI_Assemblage = line['status_count']
                nbr_sav_cloture += pending_DSI_Assemblage
            elif line['statut'] == 'Terminé':
                termine = line['status_count']
                nbr_sav += termine
            elif line['statut'] == 'Sav livré':
                sav_livre = line['status_count']
                nbr_sav += sav_livre
            elif line['statut'] == 'Sav non livré':
                sav_non_livre = line['status_count']
                nbr_sav += sav_non_livre
            elif line['statut'] == 'Sav payé':
                sav_paye = line['status_count']
                nbr_sav += sav_paye
            elif line['statut'] == 'Sav non payé':
                sav_non_paye = line['status_count']
                nbr_sav += sav_non_paye
            elif line['statut'] == 'Dossier HP à completer': 
                Dossier_HP = line['status_count']
                nbr_sav += Dossier_HP
            elif line['statut'] == 'Dossier clôturé et payé':
                Dossier_cloture_paye = line['status_count']
                nbr_sav += Dossier_cloture_paye


        # Calculate percentages
        total_requests = diagnostique_interne + pending_achat + commande_placee + \
                        pending_logistique + reception_depot_france + reception_depot_dubai + \
                        sous_douane_malienne + pending_DSI_Assemblage + nbr_sav_cloture + \
                        sav_non_paye + sav_paye + sav_non_livre + sav_livre + termine + Dossier_HP + \
                        Dossier_cloture_paye

        if total_requests == 0:
            total_requests = 1

        progress = {
            'diagnostique_interne': int(diagnostique_interne / total_requests * 100),
            'Dossier_HP': int(Dossier_HP / total_requests * 100 ),
            'pending_achat': int(pending_achat / total_requests * 100),
            'commande_placee': int(commande_placee / total_requests * 100),
            'pending_logistique': int(pending_logistique / total_requests * 100),
            'reception_depot_france': int(reception_depot_france / total_requests * 100),
            'reception_depot_dubai': int(reception_depot_dubai / total_requests * 100),
            'sous_douane_malienne': int(sous_douane_malienne / total_requests * 100),
            'pending_DSI_Assemblage': int(pending_DSI_Assemblage / total_requests * 100),
            'termine': int(termine / total_requests * 100),
            'sav_livre': int(sav_livre / total_requests * 100),
            'sav_non_livre': int(sav_non_livre / total_requests * 100),
            'sav_paye': int(sav_paye / total_requests * 100),
            'sav_non_paye': int(sav_non_paye / total_requests * 100),
            'Dossier_cloture_paye': int(Dossier_cloture_paye/ total_requests * 100),
        }

        
        # Aggregate SAV requests per client and count them
        client_agg = Client_sav.objects.annotate(
            sav_count=Count('sav_request')
        ).filter(created_at__gte=date_old_days_ago)

        # Now iterate over client_agg to add any additional data
        for row in client_agg:
            # Get the responsible SAV name (resp_sav) for each SAV request
            resp_sav = Sav_request.objects.filter(client_sav=row.idclient).select_related('resp_sav').values('resp_sav__nom', 'resp_sav__prenom', 'statut')
            
            if resp_sav.exists():
                # Assuming the latest responsible SAV is what you want to display
                row.resp_sav_name = f"{resp_sav[0]['resp_sav__nom']} {resp_sav[0]['resp_sav__prenom']}"
            else:
                row.resp_sav_name = "N/A"

            # Determine the client name based on whether it's a company or an individual
            if row.est_personne_morale:
                row.client_name = row.raison_sociale
            else:
                row.client_name = f"{row.nom} {row.prenom}"
            
    except Exception as e:
        print(f"Error: {e}")
        
    all_sav_details = Sav_request.objects.filter(created_at__gte=date_old_days_ago).select_related('client_sav', 'resp_sav')
    
    context = {
        'nbr_sav': nbr_sav,
        'total_requests':total_requests,
        'sav_requests':all_sav_details,
        'total_sav':all_sav_details.count() or 0,
        'nbr_sav_cloture': Dossier_cloture_paye,
        'detail_status_sav':detail_status_sav,
        'agg_status_SAV':agg_status_SAV,
        'client_agg':client_agg,
        'date_old_days_ago': date_old_days_ago,  
        'today_date':  today_date,  
        'progress': progress,
        'diagnostique_interne': diagnostique_interne,
        'pending_achat': pending_achat,
        'commande_placee': commande_placee,
        'pending_logistique': pending_logistique,
        'reception_depot_france': reception_depot_france,
        'reception_depot_dubai': reception_depot_dubai,
        'sous_douane_malienne': sous_douane_malienne,
        'pending_DSI_Assemblage': pending_DSI_Assemblage,
        'termine': termine,
        'sav_livre': sav_livre,
        'sav_non_livre': sav_non_livre,
        'sav_paye': sav_paye,
        'sav_non_paye': sav_non_paye,
        'Dossier_HP': Dossier_HP,
        'Dossier_cloture_paye': Dossier_cloture_paye,
        'nbr_sav': nbr_sav,
        'row': row,
        'page':'dashboard',
        'subpage':'sav_tab',

    } 

    #return render(request, 'layout/base_2.html', context)
    ##########
    html_template = loader.get_template('servicedsi/index.html')
    return HttpResponse(html_template.render(context, request))
    
    

@login_required
# @user_passes_test(is_staff_or_superuser)
def client_sav(request):
    clients = Client_sav.objects.filter(is_active=True, is_deleted=False).select_related('customer')

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

    if request.method == "POST" and 'add_client' in request.POST:
        est_personne_morale = request.POST.get('est_personne_morale') == 'on'
        raison_sociale = request.POST.get('raison_sociale', '')
        telephone = request.POST.get('telephone', '')
        adresse = request.POST.get('adresse', '')
        nom = request.POST.get('nom', '')
        prenom = request.POST.get('prenom', '')
        user_log_id = request.POST.get('userLog', '')

        customer = get_object_or_404(Customer, id=user_log_id)
        
        
        # Check if a client with the same attributes already exists
        if Client_sav.objects.filter(customer=customer,telephone=telephone).exists():
            messages.error(request, "A client with the same details already exists!")
            return redirect('serviceapresvente:clients')
        
        try:
            with transaction.atomic():
                client = Client_sav(
                    est_personne_morale=est_personne_morale,
                    raison_sociale=raison_sociale,
                    telephone=telephone,
                    adresse=adresse,
                    client_name=f"{nom} {prenom}",
                    customer=customer,
                    nom=nom,
                    prenom=prenom,
                    userLog=request.user.email,
                )
                client.save()

                # SAV client account creation email
                template = 'email/user_created.html'
                context = {
                    'client_name': f"{nom} {prenom}",
                    'username': customer.username,
                    'created_by': request.user.email,
                }
                recievers = [customer.email]
                subject = _('client Created')

                # Send email (only pass simple data to the email function)
                send_email_with_template_customer.delay(subject, template, context, recievers, from_email)

                messages.success(request, f"Client added successfully!")
                return redirect('serviceapresvente:clients')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('serviceapresvente:clients')


    return render(request, "servicedsi/index.html", {
        'page': 'clients',
        'subpage': 'client_tab',
        'clients': clients,
        'customers': customers
    })
    
   
def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_or_superuser)
def update_client_sav(request, client_id):
    client = get_object_or_404(Client_sav, idclient=client_id)
    related_customers_ids = Client_sav.objects.exclude(idclient=client_id).values_list('customer_id', flat=True)
    customers = Customer.objects.filter(
        is_active=True,
        is_deleted=False,
        is_superuser=False
    ).exclude(id__in=related_customers_ids)

    if request.method == "POST":
        try:
            with transaction.atomic():
                client.est_personne_morale = request.POST.get('est_personne_morale') == 'on'
                client.raison_sociale = request.POST.get('raison_sociale', '')
                client.telephone = request.POST.get('telephone', '')
                client.adresse = request.POST.get('adresse', '')
                client.nom = request.POST.get('nom', '')
                client.prenom = request.POST.get('prenom', '')
                client.client_name = f"{client.nom} {client.prenom}"
                
                user_log_id = request.POST.get('userLog', '')
                if user_log_id:
                    client.customer = get_object_or_404(Customer, id=user_log_id)

                client.save()
                messages.success(request, "Client updated successfully!")
                return redirect('serviceapresvente:clients')
        except Exception as e:
            # Log the exception if needed
            messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request, "servicedsi/index.html", {
        'client': client,
        'customers': customers,
        'page': 'clients',
        'subpage': 'client_tab',
    })

@login_required
@user_passes_test(is_staff_or_superuser)
def delete_client_sav(request, client_id):
    client = get_object_or_404(Client_sav, idclient=client_id)

    if request.method == "POST":
        try:
            with transaction.atomic():
                client.is_deleted = True
                client.is_active = False
                client.save()
                messages.success(request, "Client deleted successfully!")
                return redirect('serviceapresvente:clients')
        except Exception as e:
            # Log the exception if needed
            messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request, "servicedsi/index.html", {
        'client': client,
        'page': 'clients',
        'subpage': 'client_tab',
    })
    
    
    
@login_required
def dashboard_leasing(request):
    context = {'segment': 'index'}
    AllImp = ''
    refAgg = ''
    ImprimanteDeploye = 0
    ImprimanteNonDeploye = 0
    RefImpStatut = ''
    clientleasing = Clientleasing.objects.all()
    Nbre_Client_Nbr_Impr = Deploiement.select_Nbre_Client_Impr()
    AllImp,refAgg,ImpStatus,RefImpStatut = Listeimprimante.LeasingStatImprimante()
    deploieClientSiteImp = Deploiement.objects.values('clientleasing__nom','site','listeimprimante__reference').annotate(nombreImprimante=Count('listeimprimante__reference')).order_by('clientleasing__nom','site')
    #print('AllImp:',AllImp)
    #print('refAgg:',refAgg)
    #print('ImpStatus:',ImpStatus)
    #print('RefImpStatut:',RefImpStatut)
    conso = Consommable.select_conso_stock()
    consomTab=[]
    #print('conso:',conso)
    for row in conso:
        detail = {
            'modeleimprimante': row['modeleimprimante'] ,
            'produit': row['produit'] ,
            'reference': row['reference'] ,
            'stock': row['stock'] ,
            'seuilLimite': row['seuilLimite'] ,
        }
        consomTab.append(detail)
    lientLeasingTab = []
    #print('clientleasing:',clientleasing)
    for row in clientleasing:
        detail = {
            'name':row.nom
        }
        lientLeasingTab.append(detail)
    #print('lientLeasingTab:',lientLeasingTab)
    refAggTab = []
    for row in refAgg:
        detail = {
            'reference':row['reference'],
            'nombre':row['status_count']
        }
        refAggTab.append(detail)
    for row in ImpStatus:
        if row['flag'] == False:
            ImprimanteNonDeploye =  row['status_count'] 
        if row['flag'] == True: 
            ImprimanteDeploye =  row['status_count'] 
            #print('ImprimanteDeploye:',ImprimanteDeploye)
    RefImpStatutTab = []
    for row in RefImpStatut:
        if row['flag'] == False:
                status= 'Non déployée'
        else: 
            status = 'deployée'        
        detail = {
            'reference':row['reference'],
            'flag': status,
            'nombre':row['status_count']
        }
        RefImpStatutTab.append(detail)
    #print('RefImpStatutTab:',RefImpStatutTab)
    deploieClientSiteImpTab = []
    for row in deploieClientSiteImp:
        detail = {
            'client':row['clientleasing__nom'],
            'site':row['site'],
            'reference':row['listeimprimante__reference'],
            'nombre':row['nombreImprimante']
        }
        deploieClientSiteImpTab.append(detail)
    context={
            'lientLeasingTab':lientLeasingTab,
            'Nbre_Client_Nbr_Impr':Nbre_Client_Nbr_Impr,
            'NbreImpr':AllImp,
            'ImprimanteDeploye':ImprimanteDeploye,
            'ImprimanteNonDeploye':ImprimanteNonDeploye,
            #'refAggTab':refAggTab,
            'RefImpStatutTab':RefImpStatutTab,
            'deploieClientSiteImpTab':deploieClientSiteImpTab,
            'consomTab':consomTab,
            'page':'dashboard',
            'subpage':'leasing_tab',

            
        }
    html_template = loader.get_template('servicedsi/index.html')
    return HttpResponse(html_template.render(context, request))

    
@login_required
def dashboard_instance(request):
    
     # Query for paid and unpaid invoices based on their status
    paid_invoices = Instance.objects.filter(statut=Instance.STATUS.CLOTURE)
    unpaid_invoices = Instance.objects.filter(statut__in=[Instance.STATUS.EN_COURS, Instance.STATUS.NON_RESOLU])

    # Calculate the number of paid and unpaid invoices
    nbr_facture_paye = paid_invoices.count()
    nbr_facture_non_paye = unpaid_invoices.count()

    # Calculate the total amount of paid and unpaid invoices (assuming you store the amount somewhere)
    # Here, assuming `montant` is a field in the `Instance` model:
    nbr_facture_paye_montant = sum(instance.rapport_technique.amount for instance in paid_invoices if instance.rapport_technique)  # Replace rapport_technique.amount with actual amount field if any
    nbr_facture_non_paye_montant = sum(instance.rapport_technique.amount for instance in unpaid_invoices if instance.rapport_technique)


    context ={
        'all_instances': Instance.objects.values_list('idinstance', flat=True).count(),
        'instance_en_cour': Instance.objects.filter(
                                Q(statut='En cour') | 
                                Q(statut='Recouvrement') |
                                Q(statut='Décision DG') |
                                Q(statut='Non résolu'),
                            ).values_list('idinstance', flat=True).count(),
        'Instance_Interne': Instance.objects.filter(type_instance='Interne'), 
        'Instance_Externe': Instance.objects.filter(type_instance='Externe'), 
        'nbr_facture_paye': nbr_facture_paye,
        'nbr_facture_paye_montant': nbr_facture_paye_montant,
        'nbr_facture_non_paye': nbr_facture_non_paye,
        'nbr_facture_non_paye_montant': nbr_facture_non_paye_montant,
        'page':'dashboard',
        'subpage':'instance_tab',

         }
    
    return render(request,"servicedsi/index.html", context)
        

def jsonInstance(request):
    details = []
    response_data=''
    try:
        status = request.GET.get('status')
        dept = request.GET.get('dept')
        resp = request.GET.get('resp')
        
        dept2 = Personnels.objects.filter(idpersonnel=dept).values('iddept')
        dept_id = dept2[0]['iddept']
        if status=='Interne':
            #print("status:",status)
            #print("dept:",dept_id)
            #print("resp:",resp)
            response_data = Instance.detail_instance_interne(status,dept_id,resp)
            detailsInterne=[]
            if response_data:
                #print('response_data:',response_data)
                
                for rows in response_data:
                    detail = {
                        'departement': rows.departement.departement,
                        'responsable': rows.responsable,
                        'numero_dossier': rows.numero_dossier,
                        'actions': rows.actions,
                        'description': rows.description,
                        'status': rows.status,
                        'date_action': rows.date_action,
                        'observation': rows.observation,
                        }
                    detailsInterne.append(detail)
                        #print('details:',details)
                #print('detailsInterne:',detailsInterne)
            Jsonresult={
                            'details_interne': detailsInterne,
                        }
            return JsonResponse(Jsonresult, safe=False)
    
        if status=='Externe':
            # Filtrez les instances avec les factures associées par type_instance, departement et responsable
            instances_with_recouvrement = Instance.objects.filter(
                type_instance='Externe',
                departement= dept_id,
                responsable= resp
            ).prefetch_related(
                Prefetch('sav_instance_recouvrement_set',queryset=Instance_recouvrement.objects.all())
            )
            #print('result instances_with_recouvrement:', instances_with_recouvrement)
            detailsExterne =[]
            for instance in instances_with_recouvrement:
              #print(f"Instance ID: {instance.idinstance}")
              for recouvrement in instance.sav_instance_recouvrement_set.all():
                  detail = {
                        'departement': instance.departement.departement,
                        'responsable': instance.responsable,
                        'numero_dossier': instance.numero_dossier,
                        'actions': instance.actions,
                        'description': instance.description,
                        'status': instance.status,
                        'date_action': instance.date_action,
                        'observation': instance.observation,
                        'facture_reference': recouvrement.facture_reference,
                        'facture_montant': recouvrement.facture_montant,
                        'facture_paiement': recouvrement.facture_paiement,
                       }
                  #print(f"  Facture référence: {recouvrement.facture_reference}")
                  #print(f"  Montant: {recouvrement.facture_montant}")
                  #print(f"  Paiement: {recouvrement.facture_paiement}")
                  
                  detailsExterne.append(detail)
            #print('detailsExterne:',detailsExterne)
            Jsonresult={
                    'details_externe': detailsExterne,
                        }
            #print('Jsonresult',Jsonresult)
            return JsonResponse(Jsonresult, safe=False) 
        
    except Exception as e:
        print(e)
        return JsonResponse({'erreur': 'Erreur de décodage JSON', 'details': str(e)}, status=400)   
    return JsonResponse({'JSON': 'Aucun traitement'})   
    
    
    
    
    
    
  