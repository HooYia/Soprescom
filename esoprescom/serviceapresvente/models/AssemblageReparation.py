from django.db import models
from datetime import datetime,timedelta,date
from django.db.models import Count,Sum, Case, When, Sum
from django.utils.translation import gettext_lazy as _
from serviceapresvente.models.SuiviCommandeSav import  SuiviCommandeSav
from django.core.validators import MaxLengthValidator


#########################
#Assemblage Reparation  #
#########################
class AssemblageReparation(models.Model):
    class ETAT(models.TextChoices):
        DEFAULT="pending (DSI - Assemblage)","pending (DSI - Assemblage)"
        TERMINER="Terminé","Terminé"
    idassemblage = models.BigAutoField(primary_key=True)
    suivicommandesav = models.OneToOneField(SuiviCommandeSav, on_delete=models.CASCADE,related_name='suivicommandesavs')
    statut = models.CharField(max_length=30,verbose_name =_('Statut'),
                                    choices=ETAT.choices,default=ETAT.DEFAULT)
    commentaire = models.TextField(
                  null=True,
                  blank=True,
                  validators=[MaxLengthValidator(limit_value=200)] )
    flag = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
         return '{}'.format(self.suivicommandesav) 
       