from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.accounts.models import Profile

class Customer(AbstractUser):
  agree_terms = models.BooleanField(default=False)
  is_compta = models.BooleanField(default=False)
  is_losgistic = models.BooleanField(default=False)
  is_recouvrement = models.BooleanField(default=False)
  is_leasing = models.BooleanField(default=False)
  is_instance = models.BooleanField(default=False)
  is_stock = models.BooleanField(default=False)
  is_leasing2 = models.BooleanField(default=False)
  is_deleted = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
