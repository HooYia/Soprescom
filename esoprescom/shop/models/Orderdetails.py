from django.db import models
from shop.models.Order import Order


class Orderdetails(models.Model):
    product_name        = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255)
    solde_price         = models.FloatField()
    regular_price       = models.FloatField()
    quantity            = models.IntegerField()
    taxe                = models.IntegerField()
    sub_total_ht        = models.FloatField()
    sub_total_ttc       = models.FloatField()
    updated_at          = models.DateTimeField(auto_now=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    # Relation avec le model Order
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_details')

    def __str__(self):
      return f"Orderdetail {self.id} - {self.product_name}"
