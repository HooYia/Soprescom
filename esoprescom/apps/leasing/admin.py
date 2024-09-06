from django.contrib import admin
from .models import Clientleasing, Listeimprimante,Consommable,Deploiement,Exploitation
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
#from .models.Client import Client
#from .models.Listeimprimante import Listeimprimante
#from .models.Consommable import Consommable
#from .models.Deploiement import Deploiement
#from .models.Exploitation import Exploitation


####### Client Leasing
@admin.register(Clientleasing)
class LeasingClientAdmin(admin.ModelAdmin):
   list_display=( "date","nom","refcontrat","duree_contrat","contact","localite")
   list_display_links = ('nom',)
   list_editable = ("duree_contrat","contact")
   
####### Imprimante
@admin.register(Listeimprimante)
class ImprimanteAdmin(admin.ModelAdmin):
   list_display=( "numero_serie","reference","designation","date_acquisition","garantie",'display_image')
   list_display_links = ('reference',)
    
   empty_value_display = "Inconnu"
   list_editable = ("designation","garantie")

   def display_image(self,obj):
      return format_html(f'<img src="{obj.image.url}" width=80')
   display_image.short_description = 'image'


####### Consommable
@admin.register(Consommable)
class ConsommableAdmin(admin.ModelAdmin):
   list_display=("marque","modeleimprimante","produit","reference","designation","quantite","display_image")
   list_display_links = ("modeleimprimante","produit")
   empty_value_display = "Inconnu"
   list_editable = ("designation","quantite")

   def display_image(self,obj):
      return format_html(f'<img src="{obj.image.url}" width=80')
   display_image.short_description = 'image'

####### Deploiement
@admin.register(Deploiement)
class DeploiementAdmin(admin.ModelAdmin):
   list_display=("iddeploiement","clientleasing_id","site","adresseip",'date_deploiement',
                 "listeimprimante_id",)
   list_display_links = ("clientleasing_id",)
   empty_value_display = "Inconnu"
   list_editable = ("site","adresseip")

#######Exploitation
@admin.register(Exploitation)
class ExploitationAdmin(admin.ModelAdmin):
   list_display=("date_exploitation","intervention","display_consommables")
                 
   list_display_links = ("intervention",)
 
   empty_value_display = "Inconnu"
   

   # Méthode pour afficher les consommables
   def display_consommables(self, obj):
        # Récupère tous les consommables associés et les renvoie sous forme de liste jointe
        return ", ".join([consommable.reference for consommable in obj.consommables.all()])

   display_consommables.short_description = "Consommables"
