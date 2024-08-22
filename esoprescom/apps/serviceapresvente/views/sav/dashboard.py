from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from datetime import datetime,timedelta

import json
from django.http import JsonResponse
from apps.serviceapresvente.models import Sav_request,Instance,Client_sav,Personnels, \
                            Instance_recouvrement
from apps.leasing.models import *
from django.db.models import F    
from django.db.models import OuterRef, Subquery               
from apps.serviceapresvente.models import *
from django.core.serializers import serialize
from django.db.models import Prefetch

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render



today_date = datetime.now()
date_old_days_ago = datetime.now() - timedelta(days=180)

@login_required
def dashboard(request):
    
    context = {'segment': 'index'}
    ##########
    """Dashboard page """
    diagnostiqueinterne = 0
    validationfactureclient = 0
    commandeFournisseur = 0
    commandeFournisseurplacee  = 0
    eninstanceAssemblage = 0
    assemblage = 0
    eninstancedelivraison = 0
    eninstancederecouvrement = 0
    dossierClotute = 0
    nbr_sav = 0
    nbr_sav_cloture = 0
    nbr_client_sav = 0
    nbr_client_sav_cloture = 0
    agg_status_SAV = ''
    detail_status_sav =''
    client_agg=''
    ##########
    try:
        agg_status_SAV,detail_status_sav = Sav_request.sav_query_instance()
        client_agg = Sav_request.sav_query_client()
        #print('client_agg: ',client_agg)
        print("agg_status_SAV:",agg_status_SAV)
        for line in detail_status_sav:
            Name = Personnels.objects.filter(idperso=line['resp_sav']).values('nom','prenom')
            if Name:
                for row in Name:
                    line['resp_sav_name'] = row['nom'] +' '+row['prenom']   
        #print("detail_status_sav:",detail_status_sav)
        progress = []
        for line in agg_status_SAV:
            if line['status'] =='Diagnostique interne':
                diagnostiqueinterne  = line['status_count']
                nbr_sav += diagnostiqueinterne
            elif line['status'] == 'Validation facture client':
               validationfactureclient = line['status_count']
               nbr_sav +=validationfactureclient
            elif line['status'] == 'Commande Fournisseur':
               commandeFournisseur = line['status_count']
               nbr_sav +=commandeFournisseur
            elif line['status'] == 'Commande Fournisseur placée ':
               commandeFournisseurplacee = line['status_count'] 
               nbr_sav +=commandeFournisseurplacee
            elif line['status'] == 'En instance d\'Assemblage ':
               eninstanceAssemblage = line['status_count'] 
               nbr_sav +=eninstanceAssemblage        
            elif line['status'] == 'En instance de livraison':
                eninstancedelivraison = line['status_count']
                nbr_sav +=eninstancedelivraison
            elif line['status'] == 'En instance de recouvrement':
                eninstancederecouvrement = line['status_count']
                nbr_sav +=eninstancederecouvrement
            elif line['status'] == 'Dossier Clôtuté':
                dossierClotute = line['status_count'] 
                nbr_sav_cloture += dossierClotute
        detail= {
            'diagnostiqueinterne':diagnostiqueinterne,
            'validationfactureclient':validationfactureclient,
            'commandeFournisseur':commandeFournisseur,
            'commandeFournisseurplacee':commandeFournisseurplacee,
            'eninstanceAssemblage':eninstanceAssemblage,
            'eninstancedelivraison':eninstancedelivraison,
            'eninstancederecouvrement':eninstancederecouvrement,
            'dossierClotute':dossierClotute,
        }
        progress.append(detail)
        
        for row in client_agg:
            #print('row:',row['client_sav']) 
            client = Client_sav.objects.filter(idclient = row['client_sav']).values('nom','prenom','raison_sociale','est_personne_morale')  
            for line in client:
                #print('est_personnemorale:',line['est_personne_morale'])
                if line['est_personne_morale']:
                    row['client_name']= line['raison_sociale']
                else:
                    row['client_name']= line['nom']+' '+line['prenom']
                    
            Name = Personnels.objects.filter(idperso=row['resp_sav']).values('nom','prenom')
            if Name:
                for line in Name:
                    row['resp_sav_name'] = line['nom'] +' '+line['prenom']    
            #print('client_agg:',client_agg)                  
            #print('detail_status_sav:',detail_status_sav)                  
    except Exception as e:
        print(e)     
    context = {
      'nbr_sav': nbr_sav,
      'nbr_sav_cloture':nbr_sav_cloture,
      'detail_status_sav':detail_status_sav,
      'agg_status_SAV':agg_status_SAV,
      'client_agg':client_agg,
      'date_old_days_ago': date_old_days_ago,  
      'today_date':  today_date,  
      'diagnostiqueinterne':diagnostiqueinterne,
      'validationfactureclient':validationfactureclient,
      'commandeFournisseur':commandeFournisseur,
      'commandeFournisseurplacee':commandeFournisseurplacee,
      'eninstanceAssemblage':eninstanceAssemblage,
      'eninstancedelivraison':eninstancedelivraison,
      'eninstancederecouvrement':eninstancederecouvrement,
      'dossierClotute':dossierClotute,
      'page':'dashboard',
      'subpage':'sav_tab',

    } 

    #return render(request, 'layout/base_2.html', context)
    ##########
    html_template = loader.get_template('servicedsi/index.html')
    return HttpResponse(html_template.render(context, request))
    
    

@login_required
def dashboard_sav(request):
    
    
    return render(request,"servicedsi/index.html",{
    'page':'dashboard',
    'subpage':'sav_tab',
    })
    
    
@login_required
def dashboard_leasing(request):
    
    
    return render(request,"servicedsi/index.html",{
    'page':'dashboard',
    'subpage':'leasing_tab',
    })
    
    
@login_required
def dashboard_instance(request):
    
    
    return render(request,"servicedsi/index.html",{
    'page':'dashboard',
    'subpage':'instance_tab',
    })