from django.contrib import admin
from django.utils.html import format_html
from apps.shop.models.Collection import Collection
from apps.shop.models.Slider import Slider
from apps.shop.models.Product import Product, Stock
from apps.shop.models.Category import Category
from apps.shop.models.Image import Image
from apps.shop.models.Setting import Setting
from apps.shop.models.Social import Social
from apps.shop.models.Page import Page
from apps.shop.models.NavCollection import NavCollection
from apps.shop.models.Carrier import Carrier
from apps.shop.models.Order import Order
from apps.shop.models.Method import Method
from apps.shop.models.Orderdetails import Orderdetails
from ckeditor.widgets import CKEditorWidget
from django.db import models

admin.site.register(Stock)


class SliderAdmin(admin.ModelAdmin):
     list_display =('id','title','description','display_image')
     list_display_links = ('title',)
     def display_image(self,obj):
      return format_html(f'<img src="{obj.image.url}" width=100')



class CollectionAdmin(admin.ModelAdmin):
     list_display =('id','title','description','display_image')
     list_display_links = ('title',)
     
     def display_image(self,obj):
        return format_html(f'<img src="{obj.image.url}" width=100')
     display_image.short_description = 'image'

class NavCollectionAdmin(admin.ModelAdmin):
     list_display =('id','title','description','display_image')
     list_display_links = ('title',)
     
     def display_image(self,obj):
        return format_html(f'<img src="{obj.image.url}" width=100')
     display_image.short_description = 'image' 
         
class CategoryAdmin(admin.ModelAdmin):
     list_display =('id','name','is_mega','description','display_image')
     list_display_links = ('name',)
     list_editable = ('is_mega',)
     exclude = ('slug',)
     
     def display_image(self,obj):
        return format_html(f'<img src="{obj.image.url}" width="50" height="40" ')
     display_image.short_description = 'image'

class ImageInline(admin.TabularInline):
     model = Image
     extra = 3

     
class ProductAdmin(admin.ModelAdmin):
     inlines = [ImageInline]
     list_display =('id','name','solde_price','regular_price','is_best_seller','is_new_arrival','is_featured','is_special_offer','display_image')
     list_display_links = ('name',)
     list_editable = ('is_best_seller','is_new_arrival','is_featured',)
     exclude = ('slug',)
     list_per_page = 5
     list_filter = ('name','created_at','updated_at')
     search_fields = ('name',)
     formfield_overrides = {
          models.TextField : {'widget':CKEditorWidget}     
     }
     
     
     def display_image(self,obj):
          first_image = obj.images.first()
          if not first_image:
               return ''
          return format_html(f'<img src="{first_image.image.url}" height = "70"  width="80"')
     display_image.short_description = 'image'

class SettingAdmin(admin.ModelAdmin):
     list_display =('id','name','description','display_logo','currency','street','city','email','phone')
     list_display_links = ('name',)
     
     def display_logo(self,obj):
        return format_html(f'<img src="{obj.logo.url}" width=100')

     display_logo.short_description = 'logo'

class SocialAdmin(admin.ModelAdmin):
     list_display =('id','name','icon','link')
     list_display_links = ('name',)


class PageAdmin(admin.ModelAdmin):
     list_display =('id','name','is_head','is_foot','is_checkout')
     list_display_links = ('name',)
     list_editable = ('is_head','is_foot','is_checkout')
     exclude = ('slug',) 
     formfield_overrides = {
          models.TextField : {'widget':CKEditorWidget}     
     }

class CarrierAdmin(admin.ModelAdmin):
     list_display =('id','name','description','price','display_image')
     list_display_links = ('name',)
     formfield_overrides = {
          models.TextField : {'widget':CKEditorWidget}     
     }
     
     def display_image(self,obj):
        return format_html(f'<img src="{obj.image.url}" width="50" height="40" ')
     display_image.short_description = 'image'


class OrderAdmin(admin.ModelAdmin):
     list_display =('id','client_name','status','billing_address','shipping_address','quantity','taxe','order_cost_ttc','is_paid','carrier_name','carrier_price','payment_method','created_at')
     list_display_links = ('client_name',)
     list_editable = ('status')
     list_filter = ('is_paid','updated_at','created_at')
     search_fields=('client_name','carrier_name')
     
class MethodAdmin(admin.ModelAdmin):
     list_display =('id','name','description','is_available','display_image')
     list_display_links = ('name',)
     list_filter = ('is_available','updated_at','created_at')
     search_fields=('name','description')
     formfield_overrides = {
          models.TextField : {'widget':CKEditorWidget}     
     }
     
     def display_image(self,obj):
        return format_html(f'<img src="{obj.logo.url}" width="50" height="40" ')
     display_image.short_description = 'logo'

          
admin.site.register(Slider,SliderAdmin)
admin.site.register(Collection,CollectionAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Setting,SettingAdmin)
admin.site.register(Social,SocialAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(NavCollection,NavCollectionAdmin)
admin.site.register(Carrier,CarrierAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Orderdetails)
admin.site.register(Method,MethodAdmin)

