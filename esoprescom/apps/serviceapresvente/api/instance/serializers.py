from rest_framework import serializers
from apps.serviceapresvente.models import Instance, Instance_recouvrement

class InstanceSerializer(serializers.ModelSerializer):
    rapport_technique_url = serializers.SerializerMethodField()

    class Meta:
        model = Instance
        fields = [
            'idinstance', 'type_instance', 'client', 'responsable', 
            'numero_dossier', 'besoin', 'action', 'statut', 
            'is_facturable', 'rapport_technique', 'rapport_technique_url', 
            'userLog', 'flag', 'flag2', 'created_at', 'updated_at'
        ]
        read_only_fields = ['idinstance', 'created_at', 'updated_at']

    def get_rapport_technique_url(self, obj):
        # Check if rapport_technique exists and return its URL
        return obj.rapport_technique.url if obj.rapport_technique else None

    def validate(self, data):
        # Add custom validation logic if needed
        return data


class InstanceRecouvrementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance_recouvrement
        fields = [
            'idrecouv', 
            'instance', 
            'facture_statut', 
            'facture_reference', 
            'facture_montant', 
            'flag', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['idrecouv', 'created_at', 'updated_at']

    def validate(self, data):
        # Add custom validation logic if needed
        return data