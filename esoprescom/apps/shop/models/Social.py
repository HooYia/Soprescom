from django.db import models

class Social(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    icon = models.CharField(max_length=100,blank=False, null=False)
    link = models.CharField(max_length=255, blank=False, null=False)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return self.name

    
