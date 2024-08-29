from django.db import models
from apps.accounts.models.Customer import Customer
from django.utils.translation import gettext_lazy as _

class Client_sav(models.Model):
    idclient = models.BigAutoField(primary_key=True)
    # Champ booléen pour indiquer le type de client
    est_personne_morale = models.BooleanField(default=False)
    raison_sociale = models.CharField(max_length=255, null=True, blank=True)
    nom = models.CharField(max_length=50,null=True, blank=True)
    prenom = models.CharField(max_length=100,null=True, blank=True)
    telephone = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    customer = models.OneToOneField(Customer, on_delete = models.PROTECT, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    userLog = models.CharField(_("User Log"), max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
       

    def __str__(self):
        if self.est_personne_morale:
            return "{}".format(self.raison_sociale)
        else:
            return f"{self.nom} {self.prenom}"  
            #return "{} - {}".format(self.nom,self.prenom)
    @property
    def name(self):   
        if self.est_personne_morale:
            return "{}".format(self.raison_sociale)
        else:
            return f"{self.nom} {self.prenom}" 
        
    def save(self, *args, **kwargs):
        if self.est_personne_morale:
            self.client_name = self.raison_sociale
        else:
            self.client_name = f"{self.nom} {self.prenom}"
        super().save(*args, **kwargs)     
