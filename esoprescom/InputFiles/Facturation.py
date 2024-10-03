from django.db import models
from datetime import datetime,timedelta,date
from django.db.models import Count,Sum, Case, When, Sum
from django.utils.translation import gettext_lazy as _
from apps.accounts.models.Customer import Customer
from apps.serviceapresvente.models.Sav_request import  Sav_request
from django.core.validators import MaxLengthValidator
from decimal import Decimal

#####################
#    Facturation  #
#####################
class Facturation(models.Model):
    idfacturation = models.BigAutoField(primary_key=True)
    savrequest = models.OneToOneField(Sav_request, on_delete=models.PROTECT)
    reference_facture = models.CharField(max_length=20,null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal('0.00'))
    facture_proforma = models.ImageField(upload_to="sav/factures/%Y/%m/%d/",blank=True, null=True)
    bon_pour_accord = models.BooleanField(
            verbose_name =_('Bon Pour Accord'),
            default=False,null=True, blank=True)
    est_paye = models.BooleanField(default=False,null=True, blank=True)
    commentaire = models.TextField(
                  null=True,
                  blank=True,
                  validators=[MaxLengthValidator(limit_value=200)] )
    flag = models.BooleanField(default=False,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        # return json.dumps(self.__dict__)
         return '{}'.format(self.date_facturation)   
    @classmethod
    def agg_query_facture_by_client(cls,param):
        queryset_paye = Facturation.objects.filter(
        savrequest__client_sav__idclient=param,
        est_paye=True
                ).values('savrequest__client_sav__idclient').annotate(
                nbr_factures_paye=Count('idfacturation'),
                total_montant_paye=Sum('montant')
            ).order_by('savrequest__client_sav__idclient')
        queryset_nonpaye = Facturation.objects.filter(
                    savrequest__client_sav__idclient=param,
                    est_paye=False
                ).values('savrequest__client_sav__idclient').annotate(
                nbr_factures_nonpaye=Count('idfacturation'),
                total_montant_nonpaye=Sum('montant')
            ).order_by('savrequest__client_sav__idclient')

        return queryset_paye,queryset_nonpaye
        
        return queryset,
    @classmethod
    def agg_query_facture(cls):
        query_facture_status = Facturation.objects.values('est_paye').annotate(
                nbr_factures=Count('est_paye'),
                total_montant=Sum('montant')
            ).order_by('est_paye')

        return query_facture_status