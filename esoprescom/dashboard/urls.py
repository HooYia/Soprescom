from django.urls import path
from dashboard.views import dashboad_views,address_views,account_views,orders_views

app_name='dashboard'

urlpatterns = [
    path('', dashboad_views.index, name='dashboard'),
    #address
    path('address', address_views.address, name='address'),
    path('address/<int:id>/edit', address_views.edit_address, name='edit-address'),
    path('address/<int:id>/remove', address_views.remove_address, name='remove-address'),
    #account
    path('account', account_views.index, name='account-detail'),
    path('account/save', account_views.save_account, name='save_account'),
    path('account/passwd_reset', account_views.reset_account_password, name='reset_account_password'),
    #orders
    path('orders', orders_views.index, name='orders'),

]