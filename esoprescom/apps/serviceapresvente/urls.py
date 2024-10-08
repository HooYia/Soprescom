from django.urls import path

#from .views.sav import Commandesav_views, Savrequest_views,Suivicommandesav_views
from .views.sav import dashboard
from apps.serviceapresvente.api.sav_api.api import *


from .views.sav import Sav_requestView,CommandeSavView, \
                   SuiviCommandeSavView,AssemblageReparationView, \
                   LivraisonView,RecouvrementView,ClotureDossierView
                   
from .views.stock import sortie_journalier, stock, product

from apps.serviceapresvente.views.sav.sortielivraison import create_sortie_livraison, delete_sortie_livraison, update_sortie_livraison
                       

from .views.instance import InstanceViews,InstancerecouvViews

app_name = 'serviceapresvente'

urlpatterns = [
    
    #dashboard
    path('', dashboard.dashboard, name='dashboard'),
    path('dashboard_leasing', dashboard.dashboard_leasing, name='dashboard_leasing'),
    path('dashboard_instance', dashboard.dashboard_instance, name='dashboard_instance'),
    
    
    #clients sav  
    path('client/', dashboard.client_sav, name='clients'),
    path('clients/update/<int:client_id>/', dashboard.update_client_sav, name='update_client_sav'),
    path('clients/delete/<int:client_id>/', dashboard.delete_client_sav, name='delete_client_sav'),

    
    
    #Gestion SAV
    #path('', Savrequest_views.index, name='sav'),
    #Sav Request
    path('dashboard/sav', Sav_requestView.index, name='savrequest'),
    path('add', Sav_requestView.create, name='savrequest-create'),
    path('<int:id>/edit', Sav_requestView.update, name='savrequest-update'),
    path('<int:id>/detail', Sav_requestView.show, name='savrequest-show'),
    path('<int:id>/detele', Sav_requestView.index, name='savrequest-delete'),
    path('<int:id>/print', Sav_requestView.telecharger_fiche_dentree_pdf, name='savrequest-download'),
    
    ## Commande sav
    path('commandesav', CommandeSavView.index, name='commandesav'),
    path('commandesav/<int:id>/edit', CommandeSavView.update, name='commandesav-update'),
    path('commandesav/<int:id>/detail', CommandeSavView.show, name='commandesav-show'),

    ## SUivi Commande sav
    path('suivicommandesav', SuiviCommandeSavView.index, name='suivicommandesav'),
    path('suivicommandesav/<int:id>/edit', SuiviCommandeSavView.update, name='suivicommandesav-update'),
    path('suivicommandesav/<int:id>/detail', SuiviCommandeSavView.show, name='suivicommandesav-show'),
    ## Assemblage
    path('assemblage', AssemblageReparationView.index, name='assemblage'),
    path('assemblage/<int:id>/edit', AssemblageReparationView.update, name='assemblage-update'),
    path('assemblage/<int:id>/detail', AssemblageReparationView.show, name='assemblage-show'),
    ## Livraison sav
    path('livraison', LivraisonView.index, name='livraison'),
    path('livraison/<int:id>/edit', LivraisonView.update, name='livraison-update'),
    path('livraison/<int:id>/detail', LivraisonView.show, name='livraison-show'),
    ## Recouvrement sav
    path('recouvrement', RecouvrementView.index, name='recouvrement'),
    path('recouvrement/<int:id>/edit', RecouvrementView.update, name='recouvrement-update'),
    path('recouvrement/<int:id>/detail', RecouvrementView.show, name='recouvrement-show'),
    ## cloture sav
    path('cloture', ClotureDossierView.index, name='cloture'),
    
    ##Gestion Instance
    path('instance', InstanceViews.index, name='instance'),
    path('instance/add', InstanceViews.create, name='instance-create'),
    path('instance/<int:id>/edit', InstanceViews.update, name='instance-update'),
    path('instance/<int:id>/detail', InstanceViews.show, name='instance-show'),
    path('instance/<int:id>/delete', InstanceViews.delete, name='instance-delete'),

    ## Gestion Instance recouvrement
    path('instancerecouv', InstancerecouvViews.index, name='instancerecouv'),
    path('instancerecouv/<int:id>/edit', InstancerecouvViews.update, name='instancerecouv-update'),
    path('instancerecouv/<int:id>/detail', InstancerecouvViews.show, name='instancerecouv-show'),

    path('create-client/', Sav_requestView.create_client, name='create_client'),

    #Gestion stock
    path('stock', stock.stock, name='stock'),
    path('stock_create/', stock.add_stock, name='add_stock'),
    path('stock/update/<int:stock_id>', stock.update_stock, name='update_stock'),
    path('stock/delete/<int:stock_id>', stock.delete_stock, name='delete_stock'),
    path('sortie-journalier', sortie_journalier.sortie_journalier, name='sotie_journalier'),
    path('product', product.product_view, name='product'),
    path('sortie/livraison/', create_sortie_livraison, name='create_sortie_livraison'),
    path('update/sortie/livraison/<int:id>', update_sortie_livraison, name='update_sortie_livraison'),
    path('delete-sortie-livraison/<int:id>/', delete_sortie_livraison, name='delete_sortie_livraison'),
    
    #Action log
    path('action-log', stock.action_log, name='action_log'),
    

   
]
