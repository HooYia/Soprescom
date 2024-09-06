from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import django.db
from django.utils.translation import gettext_lazy as _  
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models import Count,Sum, Case, When, Sum
from apps.leasing.models.Listeimprimante import Listeimprimante

User = get_user_model()

### Gestion Consommable
class Consommable(models.Model):
    class TypeConsommable(models.TextChoices):
        cartouche ="Cartouche", "Cartouche"
        photoconducteur = "Photoconducteur", "Photoconducteur"
        kits = "Kits", "Kits "
        fuser = "fuser LexMark", "Fuser LexMark"
        papier = "Papier RAM", "Papier RAM"
    class OrigineConsommable(models.TextChoices):
        hp ="HP","Produit HP"
        lexmark = "Produit LexMask","Produit LexMask"
        canon = "Produit Canon", "Produit Canon"
        AUTRE = "Autres", "Autres"
    idconsommable = models.BigAutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    bordereausortie = models.CharField(verbose_name =_('Bordereau SOP'), max_length=30,null=False, blank=False)
    categorieproduit = models.ForeignKey(Listeimprimante,verbose_name =_('Catégorie'), on_delete=models.SET_DEFAULT,null=True,blank=True,default=None)
    typeproduit = models.CharField(verbose_name =_('Produit'),unique=False, max_length=30,null=False, blank=False)
    reference = models.CharField(verbose_name =_('Référence'),unique=True, max_length=30,null=False, blank=False,db_index=True)
    designation = models.CharField(verbose_name =_('Désignation'),max_length=50,null=False, blank=False)
    description = models.CharField(verbose_name =_('Description'),max_length=100,null=True, blank=True)
    modele = models.CharField(verbose_name =_('Modele'), max_length=30,null=False, blank=False,db_index=True)
    
    quantite = models.IntegerField(verbose_name =_('Quantité'),default=0,null=False, blank=False)
    seuilLimite = models.IntegerField(verbose_name =_('Seuil'),default=5,null=False, blank=False)
    userLog = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    
    def __str__(self) -> str:
       return "{}".format(self.reference,self.quantite)
       #return "{} - {} - {}".format(self.type,self.reference,self.quantite)

    @classmethod
    def select_conso_stock(cls):
        queryset = Consommable.objects.values('categorieproduit','typeproduit','reference','seuilLimite').annotate(stock=Sum('quantite')).order_by('categorieproduit','typeproduit','reference')
        return queryset