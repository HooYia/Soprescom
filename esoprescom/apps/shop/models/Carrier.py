from django.db import models


class Carrier(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=120, blank=False, null=False)
    details = models.TextField(blank=False, null=False)
    price = models.FloatField( blank=False, null=False)
    image = models.ImageField(upload_to="carrier_images/%Y/%m/%d/", blank=False, null=False)
   
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

        
    def __str__(self):
        return f"{self.name} {self.price} FCFA"
            
