from django.db import models
from apps.accounts.models.Customer import Customer

class Order(models.Model):
    STATUS_CHOICES = [
      ('Pending','Pending'),
      ('Processing','Processing'),
      ('Shipped','Shipped'),
      ('Delivered','Delivered'),
      ('Canceled','Canceled'),
    ]
    client_name     = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)
    shipping_address= models.CharField(max_length=255)
    quantity        = models.IntegerField()
    taxe            = models.IntegerField()
    order_cost      = models.FloatField()
    order_cost_ttc =  models.FloatField()
    is_paid         = models.BooleanField(default=False)
    carrier_name    = models.CharField(max_length=50)
    carrier_price   = models.FloatField()
    payment_method  = models.CharField(max_length=50)
    strip_payment_intent  = models.CharField(max_length=255,null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # relation ave Customer
    author = models.ForeignKey(Customer,on_delete=models.PROTECT)
    
    def __str__(self):
      return f"Order {self.id} - {self.client_name}"
