from django.db import models
from datetime import datetime,timedelta,date
from django.db.models import Count,Sum, Case, When, Sum
from django.utils.translation import gettext_lazy as _
from apps.serviceapresvente.models.Instance  import Instance

### Suivi SAV recouvrement SopresCom
class Instance_recouvrement(models.Model):
    class RECOUVREMENT(models.TextChoices):
          PAYE ="Payé","Payé"
          NONPAYE = "Non Payé","Non Payé"  
        
    idrecouv = models.BigAutoField(primary_key=True)
    instance = models.ForeignKey(Instance, on_delete=models.PROTECT,null=False,db_index=True)
    facture_reference = models.CharField(verbose_name =_('N° facture'),unique=True, max_length=30,null=True, blank=True)
    facture_montant = models.FloatField(verbose_name =_('Montant'),default=0)
    facture_statut = models.CharField(max_length=20,verbose_name =_('Paiement'),
                                    choices=RECOUVREMENT.choices,default=RECOUVREMENT.NONPAYE)
    flag = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
       return "{}".format(self.idrecouv)
    
    @classmethod
    def sav_query_facture(cls):
        queryset = Instance_recouvrement.objects.values('facture_statut').annotate(
            facture_paiement_count=Count('facture_statut'),
            facture_amount=Sum('facture_montant')).order_by('facture_statut')  

        return queryset