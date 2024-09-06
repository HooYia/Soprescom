from django.contrib import admin
from django.urls import path
from .views import LeasingClientViews,ListeimprimanteViews,DeploiementViews, \
                   ConsommableViews,ExploitationViews

app_name = 'leasing'

urlpatterns = [
    #Client
    path('client', LeasingClientViews.index, name='client'),
    path('client/add/', LeasingClientViews.create, name='client-create'),
    path('client/upd/<int:id>/', LeasingClientViews.update, name='client-update'),
    path('client/detail/<int:id>/', LeasingClientViews.show, name='client-show'),
  
    #Liste Imprimante
    path('listeimp', ListeimprimanteViews.index, name='imp-list'),
    path('listeimp/add', ListeimprimanteViews.create, name='imp-create'),
    path('listeimp/upd/<int:id>/', ListeimprimanteViews.update, name='imp-update'),
    path('listeimp/detail/<int:id>', ListeimprimanteViews.show, name='imp-show'),
    #Liste Deploiement
    path('deploiement', DeploiementViews.index, name='deploiement-list'),
    path('deploiement/add', DeploiementViews.create, name='deploiement-create'),
    path('deploiement/upd/<int:id>/', DeploiementViews.update, name='deploiement-update'),
    path('deploiement/detail/<int:id>', DeploiementViews.show, name='deploiement-show'),
    #Liste Consommable
    path('consommable', ConsommableViews.index, name='consommable-list'),
    path('consommable/add', ConsommableViews.create, name='consommable-create'),
    path('consommable/upd/<int:id>/', ConsommableViews.update, name='consommable-update'),
    path('consommable/detail/<int:id>', ConsommableViews.show, name='consommable-show'),
    #Liste Exploitation
    path('exploitation', ExploitationViews.index, name='exploitation-list'),
    path('exploitation/add', ExploitationViews.create, name='exploitation-create'),
    path('exploitation/upd/<int:id>/', ExploitationViews.update, name='exploitation-update'),
    path('exploitation/detail/<int:id>', ExploitationViews.show, name='exploitation-show'),
    

]
