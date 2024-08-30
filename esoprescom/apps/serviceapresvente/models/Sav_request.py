from django.db import models
from datetime import datetime,timedelta,date
from django.db.models import Count,Sum, Case, When, Sum
from django.utils.translation import gettext_lazy as _
from apps.accounts.models.Customer import Customer
from apps.serviceapresvente.models.Personnels import  Personnels
from apps.serviceapresvente.models.Client_sav  import Client_sav
from apps.serviceapresvente.models.Partenaires import Partenaires
from django.utils.translation import gettext_lazy as _  
from django.core.validators import MaxLengthValidator
from django.db.models import Max
from django.db.models import Count, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import Send_Email,send_email_with_template,send_instance_email_with_template_task,send_email_with_template_task

from django.utils import timezone
from dateutil.relativedelta import relativedelta



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
    numero_fiche_technique = models.CharField(verbose_name =_('N° de Fiche Technique'),unique=True, max_length=30,null=True, blank=True,db_index=True)
    marque = models.ForeignKey(Partenaires, on_delete=models.PROTECT,null=False)
    client_sav = models.ForeignKey(Client_sav, on_delete=models.PROTECT, null=False, blank=False) 
    resp_sav = models.ForeignKey(Personnels, on_delete=models.PROTECT, null=False, blank=False)
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
    
    
    def save(self, *args, **kwargs):
        if not self.numero_dossier:
            last_dossier = Sav_request.objects.aggregate(Max('idrequest'))['idrequest__max'] or 0
            new_dossier_id = last_dossier + 1
            self.numero_dossier = f'SAV_{new_dossier_id:010d}'

        super(Sav_request, self).save(*args, **kwargs)



    # def save(self, *args, **kwargs):
    #     if not self.numero_dossier:
    #         last_dossier = Sav_request.objects.aggregate(Max('idrequest'))['idrequest__max'] or 0
    #         new_dossier_id = last_dossier + 1
    #         self.numero_dossier = f'SAV_{new_dossier_id:010d}'
    #     else:
    #         # Check if it's been 6 months since the last reset
    #         if self.created_at:
    #             six_months_ago = timezone.now() - relativedelta(months=6)
    #             if self.created_at < six_months_ago:
    #                 last_dossier = Sav_request.objects.aggregate(Max('idrequest'))['idrequest__max'] or 0
    #                 new_dossier_id = last_dossier + 1
    #                 self.numero_dossier = f'SAV_{new_dossier_id:010d}'
                    
    #     super(Sav_request, self).save(*args, **kwargs)

        
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
        queryset_agg = Sav_request.objects.all().select_related('client_sav').values('statut', 'idrequest').annotate(status_count=Count('statut')).order_by('statut') 
        queryset_detail = Sav_request.objects.all().select_related('client_sav').values('type_sav','resp_sav','statut', 'idrequest', 'client_sav').annotate(status_count=Count('statut')).order_by('statut')  
       
        return queryset_agg,queryset_detail

    @classmethod
    def sav_query_client(cls):
        queryset_client = Sav_request.objects.all().select_related('client_sav').annotate(status_count=Count('statut')).order_by('statut') 
        return queryset_client
    
    @classmethod
    def sav_query_2_client(cls,parm):  
        queryset_client = Sav_request.objects.all().select_related('client_sav').values('client_sav','statut').annotate(status_count=Count('statut')).order_by('statut') 
        return queryset_client
    
    @classmethod
    def sav_query_detail_status(cls,etat,resp): 
        queryset = Sav_request.objects.filter(created_at=date_old_days_ago,
                        statut = etat,
                        resp_sav=resp).order_by('-created_at', 'numero_dossier')
        return queryset
    

##############
# Les Signaux#
##############
from django.conf import settings
#@receiver(post_save, sender=Sav_test_request)
@receiver(post_save,sender=Sav_request)
def send_email_on_sav_request_created(sender, instance, created, **kwargs):
    if created:  # Vérifie si une nouvelle instance a été créée
        subject = 'Nouvelle requête SAV créée'
        """
        client_email = instance.client_sav.customer.email
        
        message = f"Une nouvelle requête SAV a été créée avec le numéro de dossier : {instance.numero_dossier}"
        from_email = 'souleymane@soprescom.net'
        to_email = [client_email,instance.resp_sav.email]  # Liste des destinataires
        try:
            #Send_Email(subject, message, from_email, to_email)
            logger.info(f"Email envoyé à {client_email} pour la nouvelle requête SAV.")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email à {client_email}: {str(e)}")
        """
        ##################
        template_name = 'email/new_sav.html'
        context= {
            'numero_dossier': instance.numero_dossier,
            'client_name': instance.client_sav.client_name,
            'marque': instance.marque.marque,
            'num_serie': instance.numero_serie,
            'defaut_sav': instance.description_piece,
            'resp_sav_name': instance.resp_sav.name,
            'resp_sav_telephone': instance.resp_sav.telephone,
             }
        to_email = [instance.client_sav.customer.email, instance.resp_sav.email]
        #print('to_email:',to_email)
        from_email = settings.EMAIL_HOST_USER
        #print('from_email:',from_email)
        send_email_with_template_task.delay(subject,template_name,context,to_email,from_email)
    elif (instance.statut == 'pending (achat)'):
        subject = 'Achat Pièce SAV'
        template_name = 'email/sav_achatpiece.html'
        context= {
            'numero_dossier': instance.numero_dossier,
            'client_name': instance.client_sav.client_name,
            'marque': instance.marque.marque,
            'num_serie': instance.numero_serie,
            'defaut_sav': instance.description_piece,
            'resp_sav_name': instance.resp_sav.name,
            'resp_sav_telephone': instance.resp_sav.telephone,
             }
        to_email = ['christianhonore2003@gmail.com']
        #print('to_email:',to_email)
        from_email = settings.EMAIL_HOST_USER
        #print('from_email:',from_email)
        send_email_with_template_task.delay(subject,template_name,context,to_email,from_email)
    elif (instance.statut == 'pending (DSI - Assemblage)'):
        subject = 'Livraison SAV'
        template_name = 'email/sav_assemblagePiece.html'
        context= {
            'numero_dossier': instance.numero_dossier,
            'client_name': instance.client_sav.client_name,
            'marque': instance.marque.marque,
            'num_serie': instance.numero_serie,
            'defaut_sav': instance.description_piece,
            'resp_sav_name': instance.resp_sav.name,
            'resp_sav_telephone': instance.resp_sav.telephone,
             }
        to_email = [instance.client_sav.customer.email,'christianhonore2003@gmail.com']
        #print('to_email:',to_email)
        from_email = settings.EMAIL_HOST_USER
        #print('from_email:',from_email)
        send_email_with_template_task.delay(subject,template_name,context,to_email,from_email)
    elif (instance.statut == 'SAV non Livré(e)'):
        subject = 'Livraison SAV'
        template_name = 'email/sav_livraison.html'
        context= {
            'numero_dossier': instance.numero_dossier,
            'client_name': instance.client_sav.client_name,
            'marque': instance.marque.marque,
            'num_serie': instance.numero_serie,
            'defaut_sav': instance.description_piece,
            'resp_sav_name': instance.resp_sav.name,
            'resp_sav_telephone': instance.resp_sav.telephone,
             }
        to_email = [instance.client_sav.customer.email,'christianhonore2003@gmail.com']
        #print('to_email:',to_email)
        from_email = settings.EMAIL_HOST_USER
        #print('from_email:',from_email)
        send_email_with_template_task.delay(subject,template_name,context,to_email,from_email)    
    elif (instance.statut == 'Dossier HP à completer' or instance.statut == 'Sav non payé'):
        subject = 'SAV recouvrement'
        template_name = 'email/sav_recouvrement.html'
        context= {
            'numero_dossier': instance.numero_dossier,
            'client_name': instance.client_sav.client_name,
            'marque': instance.marque.marque,
            'num_serie': instance.numero_serie,
            'defaut_sav': instance.description_piece,
            'resp_sav_name': instance.resp_sav.name,
            'resp_sav_telephone': instance.resp_sav.telephone,
             }
        to_email = [instance.client_sav.customer.email, 'christianhonore2003@gmail.com']
        #print('to_email:',to_email)
        from_email = settings.EMAIL_HOST_USER
        #print('from_email:',from_email)
        send_email_with_template_task.delay(subject,template_name,context,to_email,from_email)
        ##################

"""
@receiver(post_save,sender=Sav_instance)
def send_email_on_instance_created(sender, instance, created, **kwargs):
    if created:  # Vérifie si une nouvelle instance a été créée
        print('fonction d\'envoie de mail')
        subject = 'Nouvelle Instance SoPresCom  créée'
        template_name = 'sav/email/new_instance.html'
        print('instance.client_sav.nom_final:',instance.client_sav.nom_final)
        context= {
            'numero_dossier': instance.numero_dossier,
            'instance': instance.type_instance,
            'client': instance.client_sav.nom_final,
            'resp_name': str(instance.responsable) +'('+str(instance.departement)+')',
            'action': instance.actions,
            'statut': instance.status,
             }
        mail = Sav_instance.get_responsable_email(
            instance.departement,
            instance.responsable)
        print(mail[0]['email'])
        to_email = mail[0]['email']
        #print('to_email:',to_email)
        from_email = settings.EMAIL_HOST_USER
        #print('from_email:',from_email)
        send_instance_email_with_template_task.delay(subject,template_name,context,to_email,from_email)
    elif (instance.status == 'Clôturé' and instance.instance_facturable == 'Facturable'):
        subject = 'Nouvelle Instance SoPresCom pour recouvrement'
        template_name = 'sav/email/new_instance_recouvrement.html'
        #print('instance.client_sav.nom_final:',instance.client_sav.nom_final)
        context= {
            'numero_dossier': instance.numero_dossier,
            'instance': instance.type_instance,
            'client': instance.client_sav.nom_final,
            'resp_name': str(instance.responsable) +'('+str(instance.departement)+')',
            'action': instance.actions,
            'statut': instance.status,
             }
        mail = Sav_instance.get_responsable_email(
            instance.departement,
            instance.responsable)
        print(mail[0]['email'])
        to_email = [mail[0]['email'],'souleymane@soprescom.net']
        #print('to_email:',to_email)
        from_email = settings.EMAIL_HOST_USER
        #print('from_email:',from_email)
        send_instance_email_with_template_task.delay(subject,template_name,context,to_email,from_email)
    ##################

        
"""