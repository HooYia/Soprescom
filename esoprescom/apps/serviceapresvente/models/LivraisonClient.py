from django.db import models
from datetime import datetime,timedelta,date
from django.db.models import Count,Sum, Case, When, Sum
from django.utils.translation import gettext_lazy as _
from apps.serviceapresvente.models.AssemblageReparation import  AssemblageReparation
from django.core.validators import MaxLengthValidator

#####################
# Livraison client  #
#####################
class LivraisonClient(models.Model):
    class Livraison(models.TextChoices):
        LIVRE="Sav livré","Sav livré"
        NON_LIVRE="Sav non livré","Sav non livré"
    idlivraisonclient = models.BigAutoField(primary_key=True)
    assamblagereparation = models.OneToOneField(AssemblageReparation, on_delete=models.CASCADE,related_name='assamblagereparations')
    statut = models.CharField(max_length=30,verbose_name =_('Statut'),
                                    choices=Livraison.choices,default=Livraison.NON_LIVRE)
    commentaire = models.TextField(
                  null=True,
                  blank=True,
                  validators=[MaxLengthValidator(limit_value=50)] )
    flag = models.BooleanField(default=False)
    bordereau_livraison = models.ImageField(upload_to="sav/bordereau_livraison/%Y/%m/%d/",blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        # return json.dumps(self.__dict__)
         return '{}'.format(self.assamblagereparation)
