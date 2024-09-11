from rest_framework import serializers
from apps.leasing.models import *

class ClientleasingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientleasing
        fields = '__all__'
        
        
class ConsommableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consommable
        fields = '__all__'
        
        
class DeploiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deploiement
        fields = '__all__'
        
        
class ConsommableExploitationSerializer(serializers.ModelSerializer):
    consommable = ConsommableSerializer()

    class Meta:
        model = ConsommableExploitation
        fields = '__all__'
        
class ExploitationSerializer(serializers.ModelSerializer):
    consommableexploitation_set = ConsommableExploitationSerializer(many=True, read_only=True)

    class Meta:
        model = Exploitation
        fields = '__all__'

    def create(self, validated_data):
        consommable_exploitation_data = self.context['request'].data.get('consommableexploitation_set', [])
        exploitation = Exploitation.objects.create(**validated_data)

        for item in consommable_exploitation_data:
            consommable = Consommable.objects.get(pk=item['consommable'])
            quantite = item['quantite']

            if quantite > consommable.quantite:
                raise serializers.ValidationError(f"Quantité de {consommable.reference} insuffisante.")
            else:
                consommable.quantite -= quantite
                consommable.save()
                ConsommableExploitation.objects.create(
                    exploitation=exploitation,
                    consommable=consommable,
                    quantite=quantite
                )

        return exploitation

    def update(self, instance, validated_data):
        consommable_exploitation_data = self.context['request'].data.get('consommableexploitation_set', [])
        instance = super().update(instance, validated_data)

        for item in consommable_exploitation_data:
            consommable = Consommable.objects.get(pk=item['consommable'])
            quantite = item['quantite']

            if quantite > consommable.quantite:
                raise serializers.ValidationError(f"Quantité de {consommable.reference} insuffisante.")
            else:
                consommable.quantite -= quantite
                consommable.save()
                ConsommableExploitation.objects.create(
                    exploitation=instance,
                    consommable=consommable,
                    quantite=quantite
                )

        return instance
    

class ClientleasingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientleasing
        fields = '__all__'
        
        
class ListeimprimanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listeimprimante
        fields = '__all__'
        
 
        
