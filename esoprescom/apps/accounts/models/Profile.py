from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    organisation = models.CharField(max_length=25, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=25, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        #return f"{self.user.username}'s profile"
        return f"{self.user.username}"
    
    @property
    def photoUrl(self):
        if self.photo:
            return self.photo.url
        return ''  # ou vous pouvez renvoyer une URL d'image par défaut ici si nécessaire

