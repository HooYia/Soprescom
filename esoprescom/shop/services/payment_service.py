
from shop.models import Method
from django.conf import settings

class StripeService:
    def __init__(self):
        # Vérifie si la méthode Stripe est disponible
        self.method = Method.objects.filter(name='Stripe').first()

    # Implémentez ici la logique de votre service
    def get_public_key(self):
        if self.method:
            return self.method.prod_public_key if not settings.DEBUG else self.method.test_public_key
        return None  # Gérer le cas ou la méthode n'est pas trouvée en base de données

    def get_private_key(self):
        if self.method:
            return self.method.prod_private_key if not settings.DEBUG else self.method.test_private_key
        return None  # Gérer le cas ou la méthode n'est pas trouvée en base de données

    