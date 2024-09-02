from rest_framework import serializers
from apps.serviceapresvente.models import Sav_request

class SavRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sav_request
        fields = '__all__'  # You can specify fields explicitly if desired