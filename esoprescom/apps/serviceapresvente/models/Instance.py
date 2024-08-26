from django.db import models
from datetime import datetime,timedelta,date
from django.db.models import Count,Sum, Case, When, Sum
from django.utils.translation import gettext_lazy as _
from apps.accounts.models.Customer import Customer
from apps.serviceapresvente.models.Personnels import  Personnels
from apps.serviceapresvente.models.Client_sav  import Client_sav
from django.core.validators import MaxLengthValidator

today_date = datetime.now()
date_old_days_ago = (datetime.now() - timedelta(days=30)).date().isoformat()

class Instance(models.Model):
    class STATUS(models.TextChoices):
          EN_COURS ="En cour","En cour"
          RECOUVREMENT ="Recouvrement","Recouvrement"
          DECISION_DG ="Décision DG","Décision DG"
          CLOTURE  = "Clôturé","Clôturé"
          NON_RESOLU = "Non résolu","Non résolu"
    class TYPE_INSTANCE(models.TextChoices):
        INTERNE ="Interne","Interne"
        EXTERNE ="Externe","Externe"
    
    idinstance = models.BigAutoField(primary_key=True)
    type_instance =  models.CharField(max_length=20,verbose_name =_('Instance'), choices=TYPE_INSTANCE.choices,default=TYPE_INSTANCE.EXTERNE)
    client = models.ForeignKey(Client_sav, on_delete=models.SET_NULL,null=True,db_index=True)
    responsable = models.ForeignKey(Personnels, on_delete=models.SET_NULL,null=True,db_index=True)
    numero_dossier = models.CharField(verbose_name =_('N° de Dossier'),unique=False, max_length=30,null=False, blank=False)
    besoin = models.CharField(verbose_name =_('Besoin'),max_length=30,null=True,blank=True,)
    action = models.TextField(verbose_name =_('Action'),unique=False, null=False, blank=False,
                              validators=[MaxLengthValidator(limit_value=100)])
    statut = models.CharField(max_length=20,verbose_name =_('Statut'), choices=STATUS.choices,default=STATUS.EN_COURS)
    is_facturable = models.BooleanField(default=False)
    rapport_technique = models.ImageField(upload_to="instance/%Y/%m/%d/",blank=True, null=True)
    userLog = models.ForeignKey(Customer, on_delete = models.SET_NULL, null=True)
    flag  = models.BooleanField(default=False)
    flag2 = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
       return f"{self.type_instance} - {self.numero_dossier} ({self.client})"    

    @property
    def rapport_techniqueUrl(self):
        try:
            return self.rapport_technique.url
        except:
            url = ''
            return url
            
    @classmethod
    def status_instance(cls):
        AggstatusInstance = cls.objects.filter(created_at=date_old_days_ago).values('statut').annotate(status_count=Count('statut')).order_by('type_instance', 'statut')
        AggInstanceInterne = cls.objects.filter(created_at=date_old_days_ago, type_instance='Interne').values('responsable', 'statut').annotate(status_count=Count('statut')).order_by('responsable', 'statut')
        AggInstanceExterne = cls.objects.filter(created_at=date_old_days_ago, type_instance='Externe').values('responsable', 'statut').annotate(status_count=Count('statut')).order_by('responsable', 'statut')
        
        return AggstatusInstance, AggInstanceInterne, AggInstanceExterne
    