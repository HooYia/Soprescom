from django.contrib import admin
from django.urls import path
from .views import * 

app_name = 'leasing'

urlpatterns = [
    # Gestion Société
    #path('',ClientListView.as_view(), name="leasing-client-list"),
    path('',CombinedListView.as_view(), name="leasing-client-list"),
    path('<int:pk>',ClientDetaiView.as_view(), name="leasing-client-detail"),
    path('create/',ClientCreateView.as_view(), name="leasing-client-create"),
    path('<int:pk>/edit/',ClientUpdateView.as_view(), name="leasing-client-edit"),
    path('<int:pk>/delete/',ClientDeleteView.as_view(), name="leasing-client-delete"),
    # Gestion Imprimante
    path('impr/',ImprListView.as_view(), name="leasing-impr-list"),
    path('impr/<int:pk>',ImprDetaiView.as_view(), name="leasing-impr-detail"),
    path('impr/create/',ImprCreateView.as_view(), name="leasing-impr-create"),
    path('impr/<int:pk>/edit/',ImprUpdateView.as_view(), name="leasing-impr-edit"),
    path('impr/<int:pk>/delete/',ImprDeleteView.as_view(), name="leasing-impr-delete"),
    # Gestion Deploiement
    path('deploie/',DeploieListView.as_view(), name="leasing-deploie-list"),
    path('deploie/<int:pk>',DeploieDetaiView.as_view(), name="leasing-deploie-detail"),
    path('deploie/create/',DeploieCreateView.as_view(), name="leasing-deploie-create"),
    path('deploie/<int:pk>/edit/',DeploieUpdateView.as_view(), name="leasing-deploie-edit"),
    path('deploie/<int:pk>/delete/',DeploieDeleteView.as_view(), name="leasing-deploie-delete"),
    # Gestion Consommation
    path('conso/',ConsoListView.as_view(), name="leasing-conso-list"),
    path('conso/<int:pk>',ConsoDetaiView.as_view(), name="leasing-conso-detail"),
    path('conso/create/',ConsoCreateView.as_view(), name="leasing-conso-create"),
    path('conso/<int:pk>/edit/',ConsoUpdateView.as_view(), name="leasing-conso-edit"),
    path('conso/<int:pk>/addstock/',Conso_ajoutstock_View.as_view(), name="leasing-conso-addstock"),
    path('conso/<int:pk>/delete/',ConsoDeleteView.as_view(), name="leasing-conso-delete"),
    
    path('conso/categorie/',get_typeProduit_by_categorie, name="leasing-conso-listeproduit"),
    # Gestion Exploitation
    path('exploi/',ExploiListView.as_view(), name="leasing-exploi-list"),
    path('exploi/<int:pk>',ExploiDetaiView.as_view(), name="leasing-exploi-detail"),
    path('exploi/create/',CreateExploitationView.as_view(), name="leasing-exploi-create"),
    #path('exploi/create/',ExploiCreateView.as_view(), name="leasing-exploi-create"),
    path('exploi/<int:pk>/edit/',ExploiUpdateView.as_view(), name="leasing-exploi-edit"),
    path('exploi/<int:pk>/delete/',ExploiDeleteView.as_view(), name="leasing-exploi-delete"),
    ### Rapport
    path('rapport/',ReportLeasing, name="leasing-rapport"),

]
