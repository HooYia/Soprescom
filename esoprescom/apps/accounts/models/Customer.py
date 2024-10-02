from django.contrib.auth.models import AbstractUser
from django.db import models

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