from rest_framework import serializers
from apps.dashboard.models.Address import Address

class AddressSerializer(serializers.ModelSerializer):
    author_full_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = Address
        fields = [
            'id',
            'name',
            'full_name',
            'street',
            'code_postal',
            'city',
            'country',
            'more_details',
            'address_type',
            'author',
            'author_full_name',
            'updated_at',
            'created_at',
        ]
        read_only_fields = ['id', 'updated_at', 'created_at']

    def validate_code_postal(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Postal code must be numeric.")
        return value
