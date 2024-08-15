from django.db import models
from django.utils.translation import gettext_lazy as _
from serviceapresvente.models.CommandeSav import  CommandeSav
from django.core.validators import MaxLengthValidator

#####################
#    Suivi Commande  #
#####################
class SuiviCommandeSav(models.Model):
    class ETAT(models.TextChoices):
          COMMANDE_LANCEE ="pending (logistique)","pending (logistique)" 
          RECEPTION_DEPOT_FR  = "Réception dépôt France ","Réception dépôt France"
          RECEPTION_DEPOT_DUBAI  = "Reception dépôt Dubaï ","Réception dépôt Dubaï"
          SOUS_DOUANE_ML= "Sous Douane Malienne","Sous Douane Malienne"
          LIVRER = "Reçu","Reçu"
    idsuivicommandesav = models.BigAutoField(primary_key=True)
    commandesav = models.OneToOneField(CommandeSav, on_delete=models.CASCADE,related_name='commandesavs')
    statut = models.CharField(max_length=30,verbose_name =_('Statut'),
                                    choices=ETAT.choices,default=ETAT.COMMANDE_LANCEE)
    flag = models.BooleanField(default=False)
    nombre_jour = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    commentaire = models.TextField(
                  null=True,
                  blank=True,
                  validators=[MaxLengthValidator(limit_value=200)] )

    def __str__(self):
       return '{}'.format(self.commandesav)
