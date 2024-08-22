from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):
  agree_terms = models.BooleanField(default=False)
  is_compta = models.BooleanField(default=False)
  is_losgistic = models.BooleanField(default=False)
  is_recouvrement = models.BooleanField(default=False)