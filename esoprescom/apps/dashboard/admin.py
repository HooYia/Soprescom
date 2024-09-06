from django.contrib import admin
from django.db import models
from apps.dashboard.models.Address import Address


class AddressAdmin(admin.ModelAdmin):
      list_display =('name','full_name','street','city')
      list_display_links = ('name',)
      list_filter =('city',)


admin.site.register(Address,AddressAdmin)
