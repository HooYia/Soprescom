
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import django.db
#from django.utils.translation import gettext as _  ugettext_lazy 
from django.utils.translation import gettext_lazy as _  
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models import Count,Sum, Case, When, Sum

User = get_user_model()

class Listeimprimante(models.Model):
    idlisteimprimante = models.BigAutoField(primary_key=True)
    numero_serie = models.CharField(verbose_name =_('Numeoro Série'),unique=True,max_length=50)
    reference = models.CharField(verbose_name =_('Référence'),max_length=50,null=False, blank=False,db_index=True)
    designation = models.CharField(verbose_name =_('Désignation'),max_length=50,null=False, blank=False,db_index=True)
    description = models.CharField(verbose_name =_('Description'),max_length=50,blank=True, null=True)
    date_acquisition = models.DateField(verbose_name =_('Date Acquisition'), blank=True, null=True)
    garantie = models.CharField(max_length=10,verbose_name =_('Garantie'), blank=True, null=True)
    endoflife = models.DateField(verbose_name =_('End of Life'), blank=True, null=True)
    flag = models.BooleanField(default=False)
    userLog = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)


    def __str__(self) -> str:
      return "{} {}".format(self.idlisteimprimante,self.designation)

    @classmethod
    def LeasingStatImprimante(cls): 
        queryset_countAll = Listeimprimante.objects.count() 
        queryset_RefAgg = Listeimprimante.objects.values(
            'reference').annotate(
                status_count=Count('reference')).order_by('reference') 
        queryset_ImpStatus = Listeimprimante.objects.values('flag').annotate(
                status_count=Count('flag')).order_by('flag')    
        queryset_Refstatus = Listeimprimante.objects.values('reference','flag').annotate(
                status_count=Count('reference')).order_by('reference')    
        
        return queryset_countAll,queryset_RefAgg,queryset_ImpStatus,queryset_Refstatus
    
