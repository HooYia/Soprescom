from django.db import models
from datetime import datetime,timedelta,date
from django.db.models import Count,Sum, Case, When, Sum
from django.utils.translation import gettext_lazy as _
from accounts.models.Customer import Customer
from serviceapresvente.models.Personnels import  Personnels
from serviceapresvente.models.Client_sav  import Client_sav
from serviceapresvente.models.Partenaires import Partenaires
from django.utils.translation import gettext_lazy as _  
from django.core.validators import MaxLengthValidator

today_date = datetime.now()
date_old_days_ago = datetime.now() - timedelta(days=180)


class Sav_request(models.Model):
    class status_sav(models.TextChoices):
          pahse1_diagnostic ="Diagnostic interne","Diagnostic interne"
          phase2_demandeveis  = "Demande devis ","Demande devis"
          Phase3_validationdevis  = "Validation client ","Validation client"
          Phase3_commande= "Commande","Comande"
          Phase4_terminer = "Cloture","Cloture"
          Phase5_echec = "Echec diagnostic ","Echec diagnostic"
    class Type_sav(models.TextChoices):
          devea ="DEVEA","DEVEA"
          non_devea = "Non DEVEA","Non DEVEA"  
    class status_garantie(models.TextChoices):
          oui ="Sous garantie","Sous garantie"
          non = "hors garantie","hors garantie"
     
    idrequest = models.BigAutoField(primary_key=True)
    type_sav =  models.CharField(max_length=20,verbose_name =_('Type SAV'),
                                    choices=Type_sav.choices,default=Type_sav.devea)
    numero_dossier = models.CharField(verbose_name =_('N° de Dossier'),unique=True, max_length=30,null=False, blank=False,db_index=True)
    marque = models.ForeignKey(Partenaires, on_delete=models.PROTECT,null=True)
    client_sav = models.ForeignKey(Client_sav, on_delete=models.SET_NULL,null=True,blank=True)
    resp_sav = models.ForeignKey(Personnels, on_delete=models.SET_NULL, null=True, blank=True)
    numero_serie = models.CharField(verbose_name =_('N° de Serie'),unique=False, max_length=30,null=True, blank=True)
    reference = models.CharField(verbose_name =_('Reference'),unique=False, max_length=30,null=True, blank=True)
    designation = models.CharField(verbose_name =_('Désignation'),unique=False,max_length=50,null=True, blank=True)
    garantie = models.CharField(max_length=20,verbose_name =_('Garantie'),
                                choices=status_garantie.choices,default=status_garantie.oui)
    description_piece = models.CharField(verbose_name =_('Descr Pièce'),max_length=100,null=True, blank=True)
    reference_piece = models.CharField(verbose_name =_('Ref Pièce'),max_length=30,null=True, blank=True)
    pop = models.CharField(verbose_name =_('POP'),max_length=30,null=False, blank=True)
    statut = models.CharField(max_length=50,verbose_name =_('Statut'),default='Diagnostique interne')
    #choices=status_sav.choices,default=status_sav.pahse1_diagnostic)
    observation = models.TextField(verbose_name =_('Observation'),null=True,blank=True,
                  validators=[MaxLengthValidator(limit_value=200)])

    rapport_technique = models.ImageField(upload_to="sav/rapport_techniques/%Y/%m/%d/",blank=True, null=True)
    facture_fournisseur = models.ImageField(upload_to="sav/facture_fournissseurs/%Y/%m/%d/",blank=True, null=True)
    facture_proforma = models.ImageField(upload_to="sav/facture_proformas/%Y/%m/%d/",blank=True, null=True)
    bon_pour_accord = models.BooleanField(default=False)  
    userLog = models.ForeignKey(Customer, on_delete = models.PROTECT, null=True)
    flag = models.BooleanField(default=False)
    recouvrement_hp = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
       return  f"{self.client_sav}: {self.numero_dossier}"

    @property
    def rapport_techniqueUrl(self):
        try:
            return self.rapport_technique.url
        except:
            url = ''
            return url
    @property
    def facture_proformaUrl(self):
        try:
            return self.facture_proforma.url
        except:
            url = ''
            return url    
    @property
    def facture_fournisseurUrl(self):
        try:
            return self.facture_fournisseur.url
        except:
            url = ''
            return url     

    
    @classmethod
    def sav_query_instance(cls):
        queryset_agg = Sav_request.objects.filter(date_reception__gte=date_old_days_ago).values('status').annotate(status_count=Count('status')).order_by('status') 
        queryset_detail = Sav_request.objects.filter(date_reception__gte=date_old_days_ago).values('type_sav','resp_sav','status').annotate(status_count=Count('status')).order_by('status')  
       
        return queryset_agg,queryset_detail

    @classmethod
    def sav_query_client(cls):
        queryset_client = Sav_request.objects.filter(date_reception__gte=date_old_days_ago).values('client_sav','resp_sav','status').annotate(status_count=Count('status')).order_by('status') 
        return queryset_client
    
    @classmethod
    def sav_query_2_client(cls,parm):  
        queryset_client = Sav_request.objects.filter(date_reception__gte=date_old_days_ago,
                                                     client_sav=parm).values('client_sav','status').annotate(status_count=Count('status')).order_by('status') 
        return queryset_client
    
    @classmethod
    def sav_query_detail_status(cls,etat,resp): 
        queryset = Sav_request.objects.filter(date_reception__gte=date_old_days_ago,
                        status = etat,
                        resp_sav=resp).order_by('-date_reception', 'numero_dossier')
        return queryset