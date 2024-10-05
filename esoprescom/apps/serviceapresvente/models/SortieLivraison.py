from django.db import models
from apps.serviceapresvente.models.Client_sav import Client_sav
from apps.accounts.models import Customer


class SortieLivraison(models.Model):
    date = models.DateField()
    ol = models.CharField(max_length=255, null=True, blank=True)
    ccial = models.CharField(max_length=255, null=True, blank=True)
    fact = models.CharField(max_length=255, null=True, blank=True)
    bdc = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='livraisons')
    reference = models.CharField(max_length=255, null=True, blank=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    nature = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    qte_dde = models.PositiveIntegerField(default=0)  
    stock_initial = models.PositiveBigIntegerField(default=0)
    observation = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(("Is delete"), default=False)
    

    class Meta:
        indexes = [
            models.Index(fields=['reference']),  
            models.Index(fields=['date']), 
        ]
        ordering = ['-date']  
    def __str__(self):
        return f"SortieLivraison {self.reference} - {self.qte_dde}"
