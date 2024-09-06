
from django.db import models
import django.db
#from django.utils.translation import gettext as _  ugettext_lazy 
from django.utils.translation import gettext_lazy as _  
from django.contrib.auth import get_user_model


User = get_user_model()

class Client(models.Model):
    idclientleasing = models.BigAutoField(primary_key=True)
    nom = models.CharField( max_length=25,unique=True, null=False, blank=False,verbose_name =_('Nom'),db_index=True) 
    adresse = models.CharField(verbose_name =_('Adresse'),max_length=100,null=False, blank=False)
    contact = models.CharField(verbose_name =_('Contact'),max_length=50,null=False, blank=False)
    localite = models.CharField(verbose_name =_('Région'),max_length=20, null=False, blank=False)
    refcontrat = models.CharField(verbose_name =_('N° Contrat '),unique=True, max_length=20, null=False, blank=False)
    duree_contrat = models.CharField(verbose_name =_('Durée Contrat '), max_length=10, null=False, blank=False)
    email  = models.EmailField(verbose_name =_('Email'),max_length=50,blank=True, null=True)
    date = models.DateField(verbose_name =_('Date Contrat'),blank=True, null=True)
    #userLog = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
      return self.nom

    @classmethod
    def select_data(cls):
        queryset = Client.objects.annotate(num_deploiements=models.Count('deploiement__clientleasing')).order_by('nom', 'num_deploiements')
        return queryset
    