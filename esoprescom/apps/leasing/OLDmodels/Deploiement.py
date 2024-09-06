from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import django.db
from django.utils.translation import gettext_lazy as _  
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models import Count,Sum, Case, When, Sum
from apps.leasing.models.Client import Client
from apps.leasing.models.Listeimprimante import Listeimprimante

User = get_user_model()

class Deploiement(models.Model):
    iddeploiement = models.BigAutoField(primary_key=True)
    clientleasing = models.ForeignKey(Client,on_delete=models.SET_NULL,null=True)
    site = models.CharField(verbose_name =_('Site'),max_length=50,null=False, blank=False,db_index=True)
    adresseip = models.CharField(verbose_name =_('Adresse IP'),max_length=50,null=True, blank=True)
    date_deploiement = models.DateField(verbose_name =_('Date Deploiement'),blank=True, null=True)
    listeimprimante = models.OneToOneField(Listeimprimante,  on_delete=models.SET_NULL,null=True)
    userLog = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
 
    def __str__(self):
        return "{} - {} - {} - {}".format(self.site,self.clientleasing,self.listeimprimante,self.adresseip)
    @property
    def listeimprimante_free(self):
        return self.get_liste_imprimantes()

    def get_liste_imprimantes(self):
        # Récupérer l'imprimante liée à ce déploiement avec flag=0 s'il existe
        if self.listeimprimante and not self.listeimprimante.flag:
            return self.listeimprimante
        return None
    
    @classmethod
    def select_data(cls):
        queryset = Deploiement.objects.values('clientleasing__nom', 'site').annotate(num_deploiements=models.Count('site')).order_by('clientleasing__nom', 'site')
        return queryset
    ##Obtenir le nombre d'imprimante par Client
    @classmethod
    def select_Nbre_Client_Impr(cls):
        queryset = Deploiement.objects.values('clientleasing__nom').annotate(nombreImprimante=models.Count('listeimprimante__reference')).order_by('clientleasing__nom')
        return queryset
