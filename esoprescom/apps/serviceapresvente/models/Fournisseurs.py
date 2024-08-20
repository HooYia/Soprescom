from django.db import models
from datetime import datetime,timedelta,date
from django.db.models import Count,Sum, Case, When, Sum
from django.utils.translation import gettext_lazy as _
from apps.accounts.models.Customer import Customer
from apps.serviceapresvente.models.Sav_request import  Sav_request
from django.core.validators import MaxLengthValidator
from decimal import Decimal

#####################
#    Fournisseurs  #
#####################
class Fournisseurs(models.Model):
    nom = models.CharField(max_length=50,null=False, blank=False)
    telephone = models.CharField("Téléphone", max_length=20)
    email = models.EmailField("E-Mail", null=True, blank=True)
    adresse = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.nom)