from django.contrib import admin

from .models import Clientleasing,Listeimprimante,Deploiement,Consommable,Exploitation,\
                  typeProduit,typeCategorie

####### Client Leasing
@admin.register(Clientleasing)
class ClientAdmin(admin.ModelAdmin):
   list_display=( "nom","adresse","contact","localite",
                 "refcontrat","email","date","userLog_id")
   
   empty_value_display = "Inconnu"
   list_editable = ("refcontrat","adresse","contact","localite")
   
####### Imprimante
@admin.register(Listeimprimante)
class ImprimanteAdmin(admin.ModelAdmin):
   list_display=( "reference","designation","description","SN",
                 "date_acquisition","garantie","endoflife","userLog_id")

    
   empty_value_display = "Inconnu"
   list_editable = ("designation","description","date_acquisition","garantie")


####### Consommable
@admin.register(Consommable)
class ConsommableAdmin(admin.ModelAdmin):
   list_display=("categorieproduit","reference","description",
                 "typeproduit","quantite","userLog_id")
 
   empty_value_display = "Inconnu"
   list_editable = ("reference","description","typeproduit","quantite")

####### Deploiement
@admin.register(Deploiement)
class DeploiementAdmin(admin.ModelAdmin):
   list_display=("iddeploiement","site","adresseip",'date_deploiement',
                 "clientleasing_id","listeimprimante_id",'userLog_id')
 
   empty_value_display = "Inconnu"
   list_editable = ("site","adresseip")

#######Exploitation
@admin.register(Exploitation)
class ExploitationAdmin(admin.ModelAdmin):
   list_display=( "idexploitation","date_exploitation","intervention",
                 "pourcentage_toner","ancien_index","nouvel_index","observation",
                 "deploiement_id" )

 
   empty_value_display = "Inconnu"
   list_editable = ("intervention","pourcentage_toner",
                    "ancien_index","nouvel_index")

admin.site.register(typeCategorie) 
admin.site.register(typeProduit) 