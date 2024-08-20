from django.db import models

class Method(models.Model):
  name             = models.CharField(max_length=255)
  description      = models.CharField(max_length=255)
  more_description = models.TextField(null=True,blank=True)
  logo             = models.ImageField(upload_to='payment_methodes/%Y/%m/%d/',blank=False,null=False)
  test_public_key  = models.CharField(max_length=255)
  test_private_key = models.CharField(max_length=255)
  prod_public_key  = models.CharField(max_length=255,blank=True,null=True)
  prod_private_key = models.CharField(max_length=255,blank=True,null=True)
  is_available     = models.BooleanField(default=False)

  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name