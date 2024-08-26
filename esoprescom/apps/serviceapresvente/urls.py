from django.urls import path

#from .views.sav import Commandesav_views, Savrequest_views,Suivicommandesav_views
from .views.leasing import Leasing_views

from .views.sav import dashboard

from .views.sav import Sav_requestView,CommandeSavView, \
                   SuiviCommandeSavView,AssemblageReparationView, \
                   LivraisonView,RecouvrementView,ClotureDossierView

from .views.instance import InstanceViews,InstancerecouvViews

app_name = 'serviceapresvente'

urlpatterns = [
    
    #dashboard
    path('', dashboard.dashboard, name='dashboard'),
    path('dashboard_sav', dashboard.dashboard_sav, name='dashboard_sav'),
    path('dashboard_leasing', dashboard.dashboard_leasing, name='dashboard_leasing'),
    path('dashboard_instance', dashboard.dashboard_instance, name='dashboard_instance'),
    
    
    #Gestion SAV
    #path('', Savrequest_views.index, name='sav'),
    #Sav Request
    path('dashboard/sav', Sav_requestView.index, name='savrequest'),
    path('add', Sav_requestView.create, name='savrequest-create'),
    path('<int:id>/edit', Sav_requestView.update, name='savrequest-update'),
    path('<int:id>/detail', Sav_requestView.show, name='savrequest-show'),
    path('<int:id>/detele', Sav_requestView.index, name='savrequest-delete'),
    
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

    #Gestion Leasingcloture
    path('leasing', Leasing_views.index, name='leasing'),

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
   
]
