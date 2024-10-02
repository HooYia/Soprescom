import json
# myapp/management/commands/load_products.py

import os,sys
import random
from django.core.management.base import BaseCommand
from django.core.files import File
import django
import random




def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    try:
        from django.conf import settings
        from apps.accounts.models.Profile import Profile
        from apps.accounts.models.Customer import Customer
        # Crée un profil pour chaque utilisateur sans profil
        for user in Customer.objects.all():
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
                print(f"Profile created for {user.username}")
    except ImportError as exc:
        print(exc)
        sys.exit(1)        


if __name__ == '__main__':
    main()    
