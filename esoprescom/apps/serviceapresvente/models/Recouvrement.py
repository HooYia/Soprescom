from django.db import models
from datetime import datetime,timedelta,date
from django.db.models import Count,Sum, Case, When, Sum
from django.utils.translation import gettext_lazy as _
from apps.serviceapresvente.models.LivraisonClient import  LivraisonClient
from django.core.validators import MaxLengthValidator


#####################
#    Recouvrement  #
#####################
class Recouvrement(models.Model):
    class etat(models.TextChoices):
        OK="Sav payé","Sav payé"
        NON_OK="Sav non payé","Sav non payé"
    class ETAT(models.TextChoices):
        DEFAULT="facturation HP, a completer","facturation HP, a completer"
        DOSSIER="Dossier HP complet","Dossier HP complet"
        OK="Dossier HP payé","Dossier HP payé"
        NON_OK="Dossier HP non payé","Dossier HP non payé"
    class TRANSIT(models.TextChoices):
        TANSIT1="TANSIT1","TANSIT1"
        TANSIT2="TANSIT2","TANSIT2"  
    idrecouvrement = models.BigAutoField(primary_key=True)
    livraisonclient = models.OneToOneField(LivraisonClient, on_delete=models.CASCADE,related_name='livraisonclients')
    is_devea_request = models.BooleanField(default=False)

    statut = models.CharField(max_length=30,verbose_name =_('Statut'),
                                    choices=etat.choices,default=etat.NON_OK)
    montant_client = models.FloatField(default=0,blank=False, null=False)
    facture_client = models.ImageField(upload_to="sav/factures/%Y/%m/%d/",blank=True, null=True)
    
    ####DEVEA
    deveaOrder  = models.CharField(verbose_name =_('Order'),max_length=30,null=False, blank=False,default="0000") 
    transitaire = models.CharField(max_length=40,verbose_name =_('Statut'),
                                     choices=TRANSIT.choices,default=TRANSIT.TANSIT1)
    numero_awd = models.CharField(verbose_name =_('Numero DHL AWD'),max_length=30,null=True, blank=True) 
    montant_prestation = models.FloatField(verbose_name =_('Montant transitaire'),default=0,null=False, blank=False) 
    remise_documentaire = models.FloatField(verbose_name =_('Remise documentaire'),default=0,null=True, blank=True) 
    droit_douane = models.FloatField(verbose_name =_('Droit douane'),default=0,null=True, blank=True) 
    transport = models.FloatField(verbose_name =_('Transport'),default=0,null=True, blank=True) 
    
    statutDevea = models.CharField(max_length=40,verbose_name =_('Statut'),
                                     choices=ETAT.choices,default=ETAT.DEFAULT)
    facture_transitaire = models.ImageField(upload_to="sav/facture_transitaire/%Y/%m/%d/",blank=True, null=True) 
    autre_piece = models.ImageField(upload_to="sav/autres_pieces/%Y/%m/%d/",blank=True, null=True)
    ###########
    commentaire = models.TextField(
                  null=True,
                  blank=True,
                  validators=[MaxLengthValidator(limit_value=50)] )
    flag = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
         return '{}-{}'.format(self.livraisonclient,self.statut)

    def get_combined_status(self):
        if not self.is_devea_request:
            return self.statut
        else:
            return self.statutDevea 