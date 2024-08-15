from django.db import models

from django.utils.translation import gettext_lazy as _
from serviceapresvente.models.Recouvrement import  Recouvrement
from django.core.validators import MaxLengthValidator


#####################
#  Cloture dossier  #
#####################
class ClotureDossier(models.Model):
    class ETAT(models.TextChoices):
        OK="clôtuté","clôturé"
        NON_OK="Non clôturé","non clôturé"
     
    idcloturedossier = models.BigAutoField(primary_key=True)
    recouvrement = models.OneToOneField(Recouvrement, on_delete=models.CASCADE,related_name='recouvrements')
    numero_dossier = models.CharField(max_length=30,verbose_name =_('Numero_Dossier'), null=False,blank=False,)
    client = models.CharField(max_length=30,verbose_name =_('Client'), default='None', null=False,blank=False,)
    resp_dossier = models.CharField(max_length=30,verbose_name =_('Resp dossier'), default='None', null=False,blank=False,)
    statut = models.CharField(max_length=30,verbose_name =_('Clôture Dossier'),null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return '{}-{}-{}'.format(self.date_cloture,self.Numero_Dossier)
    
