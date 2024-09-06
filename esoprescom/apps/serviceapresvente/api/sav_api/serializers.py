from rest_framework import serializers
from apps.serviceapresvente.models import *

class SavRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sav_request
        fields = '__all__'  # You can specify fields explicitly if desired
        
        
        
class CommandeSavSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandeSav
        fields = '__all__'
        
        
        
class SuiviCommandeSavSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviCommandeSav
        fields = ['idsuivicommandesav', 'commandesav', 'statut', 'nombre_jour']  # Only serializing necessary fields


class LivraisonClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = LivraisonClient
        fields = ['idlivraisonclient', 'assamblagereparation', 'statut', 'commentaire', 'bordereau_livraison']
        
        
class AssemblageReparationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssemblageReparation
        fields = ['idassemblage', 'suivicommandesav', 'statut', 'commentaire']
        
class ClotureDossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClotureDossier
        fields = ['idcloturedossier', 'numero_dossier', 'client', 'resp_dossier', 'statut']
        
class PersonnelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnels
        fields = ['idpersonnel', 'personnel', 'departement', 'poste', 'telephone', 'email']
        

class PartenairesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partenaires
        fields = ['idpartenaire', 'marque', 'description', 'user']

class RecouvrementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recouvrement
        fields = [
            'idrecouvrement', 'livraisonclient', 'is_devea_request', 'statut',
            'montant_client', 'facture_client', 'deveaOrder', 'transitaire',
            'numero_awd', 'montant_prestation', 'remise_documentaire', 'droit_douane',
            'transport', 'statutDevea', 'facture_transitaire', 'autre_piece',
            'commentaire', 'flag', 'updated_at', 'created_at'
        ]
        
class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = [
            'idinstance', 'type_instance', 'client', 'responsable', 'numero_dossier',
            'besoin', 'action', 'statut', 'is_facturable', 'rapport_technique', 
            'userLog', 'flag', 'flag2', 'updated_at', 'created_at'
        ]