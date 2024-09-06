from django.contrib import admin
from django.db import models
from ckeditor.widgets import CKEditorWidget
from apps.serviceapresvente.models.Sav_request import Sav_request
from apps.serviceapresvente.models.Client_sav import Client_sav
from apps.serviceapresvente.models.Fournisseurs import Fournisseurs
from apps.serviceapresvente.models.Partenaires import Partenaires
from apps.serviceapresvente.models.Personnels import Personnels

from apps.serviceapresvente.models.Instance import Instance
from apps.serviceapresvente.models.Instance_recouvrement import Instance_recouvrement
from django.utils.html import format_html

class Client_savAdmin(admin.ModelAdmin):
     list_display =('idclient','est_personne_morale','client_name','telephone','adresse')
     list_display_links = ('client_name',)
     list_filter = ('est_personne_morale','updated_at','created_at')
     list_editable = ('est_personne_morale',)

class FournisseursAdmin(admin.ModelAdmin):
     list_display =('id','nom','email','telephone','adresse','updated_at','created_at')
     list_display_links = ('nom',)
     list_filter = ('updated_at','created_at')
     #list_editable = ('nom',)


class PartenairesAdmin(admin.ModelAdmin):
     list_display =('idpartenaire','marque','description','updated_at','created_at','user')
     list_display_links = ('marque',)
     list_filter = ('updated_at','created_at')
     formfield_overrides = {
          models.TextField : {'widget':CKEditorWidget}     
     }
     #list_editable = ('bon_pour_accord',)

class PersonnelsAdmin(admin.ModelAdmin):
     list_display =('idpersonnel','personnel','poste','telephone','updated_at','created_at')
     list_display_links = ('personnel',)
     list_filter = ('updated_at','created_at')
     
class Sav_requestAdmin(admin.ModelAdmin):
     list_display =('idrequest','numero_dossier','type_sav','client_sav','resp_sav','garantie','description_piece','statut','bon_pour_accord','display_image')
     list_display_links = ('numero_dossier','type_sav','client_sav',)
     list_filter = ('bon_pour_accord','updated_at','created_at')
     list_editable = ('bon_pour_accord',)
     search_fields=('numero_dossier','type_sav')
     formfield_overrides = {
          models.TextField : {'widget':CKEditorWidget}     
     }
     
     def display_image(self,obj):
        return format_html(f'<img src="{obj.rapport_techniqueUrl}" width="50" height="40" ')
     display_image.short_description = 'rapport_technique'

class InstanceAdmin(admin.ModelAdmin):
     list_display =  ('idinstance','type_instance','client','numero_dossier','besoin','statut','is_facturable','userLog','rapport_technique','updated_at','created_at')
     list_display_links = ('type_instance','client','numero_dossier',)
     list_filter = ('type_instance','client','numero_dossier','updated_at','created_at')
     list_editable = ('is_facturable',)
     search_fields=('numero_dossier','client',)
     formfield_overrides = {
          models.TextField : {'widget':CKEditorWidget}     
     }

class Instance2Admin(admin.ModelAdmin):
     list_display =  ('idrecouv','instance','facture_reference','facture_montant','facture_statut','updated_at','created_at')
     list_display_links = ('instance','facture_reference',)
     list_filter = ('facture_reference','updated_at','created_at')
     list_editable = ('facture_montant',)
     search_fields=('facture_reference',)
     

admin.site.register(Client_sav,Client_savAdmin)
admin.site.register(Fournisseurs,FournisseursAdmin)
admin.site.register(Partenaires,PartenairesAdmin)
admin.site.register(Personnels,PersonnelsAdmin)
admin.site.register(Sav_request,Sav_requestAdmin)
admin.site.register(Instance,InstanceAdmin)
admin.site.register(Instance_recouvrement,Instance2Admin)
