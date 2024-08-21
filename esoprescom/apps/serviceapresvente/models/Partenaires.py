from django.db import models
from apps.accounts.models.Customer import Customer
from django.utils.translation import gettext_lazy as _

#####################
#    Partenaire #
#####################
class Partenaires(models.Model):
      idpartenaire = models.BigAutoField(primary_key=True)
      marque = models.CharField(verbose_name =_('Marque'),unique=True, max_length=30,null=False, blank=False) 
      description = models.TextField(verbose_name =_('Description'),max_length=200,null=True, blank=True)
      user = models.ForeignKey(Customer, on_delete = models.PROTECT,null=True)
      updated_at = models.DateTimeField(auto_now=True)
      created_at = models.DateTimeField(auto_now_add=True)
       
      def __str__(self) -> str:
       return  f"{self.marque}"  