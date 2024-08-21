from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.serviceapresvente.models.Sav_request import  Sav_request
from apps.serviceapresvente.models.Fournisseurs import  Fournisseurs
from django.core.validators import MaxLengthValidator



#####################
#    Commande Piece  #
#####################
class CommandeSav(models.Model):
    class ETAT(models.TextChoices):
        TRAITER="commande placée","commande placée"
        NON_TRAITER="pending (achat)","pending (achat)"
    idcommandesav = models.BigAutoField(primary_key=True)
    savrequest = models.OneToOneField(Sav_request, on_delete=models.CASCADE,related_name='sav_requests')
    fournisseur = models.ForeignKey(Fournisseurs, on_delete=models.SET_NULL, null=True,related_name='fournisseurs')
    nombre_jour = models.IntegerField(default=0)
    statut = models.CharField(max_length=30,verbose_name =_('Statut'),
                                    choices=ETAT.choices,default=ETAT.NON_TRAITER)
    flag = models.BooleanField(default=False)
    commentaire = models.TextField(
                  null=True,
                  blank=True,
                  validators=[MaxLengthValidator(limit_value=200)] )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        # return json.dumps(self.__dict__)
         return '{}-{}'.format(self.savrequest,self.fournisseur)
