from django.db import models
from apps.shop.models.Category import Category
from django.utils.text import slugify
from django.core.validators import MinValueValidator



class Product(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=255, blank=False, null=False, unique=True)
    description = models.CharField(max_length=255, blank=False, null=False)
    more_description = models.TextField(max_length=255, blank=True, null=True)
    additional_infos = models.TextField(max_length=255, blank=True, null=True)
    solde_price = models.FloatField( blank=False, null=False)
    regular_price = models.FloatField( blank=False, null=False)
    brand = models.CharField(max_length=60, blank=True, null=True)
    is_available = models.BooleanField(default=False,blank=False, null=False)
    is_best_seller = models.BooleanField(default=False,blank=False, null=False)
    is_new_arrival = models.BooleanField(default=False,blank=False, null=False)
    is_featured = models.BooleanField(default=False,blank=False, null=False)
    is_special_offer = models.BooleanField(default=False,blank=False, null=False)
    categories = models.ManyToManyField(Category)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug
    
    def __str__(self):
        return self.name

    
class Stock(models.Model):
    stock_produit = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    initial_quantite = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    stockLimite = models.PositiveIntegerField(default=10, validators=[MinValueValidator(0)])
    date_mvt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.stock_produit.name} - Quantite: {self.quantite} - Threshold: {self.stockLimite}"

    def is_below_threshold(self):
        #TODO: Signal -> send a message
        return self.quantite <= self.stockLimite
    
    def calculate_difference(self):
        result  = int(self.initial_quantite - self.quantite)
        return result
