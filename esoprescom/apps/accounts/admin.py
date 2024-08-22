from django.contrib import admin
from apps.accounts.models.Customer import Customer
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
      list_display =('username','email','first_name','last_name','agree_terms','is_staff' ,'is_compta','is_active', 'is_losgistic', 'is_recouvrement')
      list_filter =('is_staff', 'is_recouvrement', 'is_losgistic', 'is_compta', 'is_active')


admin.site.register(Customer,CustomUserAdmin)
