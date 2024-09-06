from django.db import models
from apps.accounts.models.Customer import Customer
from django.utils.translation import gettext_lazy as _  


class Personnels(models.Model):
    idpersonnel = models.BigAutoField(primary_key=True)
    personnel = models.ForeignKey(Customer, on_delete = models.PROTECT)
    departement  = models.CharField(verbose_name =_('Département'), max_length=30,null=True, blank=True)
    poste  = models.CharField(verbose_name =_('Poste'), max_length=30,null=True, blank=True)
    telephone  = models.CharField(verbose_name =_('Telephone'),unique=True, max_length=30,null=True, blank=True)
    email  = models.EmailField(verbose_name =_('Email'),unique=True, max_length=30,null=True, blank=True,default='sav@soprescom.net')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self) -> str:
       return  f"{self.personnel.first_name} {self.personnel.last_name} ({self.departement})"     

    @property
    def name(self):   
        return f"{self.personnel.first_name} {self.personnel.last_name} ({self.departement})"     

