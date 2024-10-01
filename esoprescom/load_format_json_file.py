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
    # Lire le fichier Excel
    # Charger le fichier JSON
    with open('ProdDatabases/products_data2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    try:
        # Supprimer les antislashs et limiter la longueur des champs "name" et "description"
        for item in data:
            if 'name' in item['fields']:
                item['fields']['name'] = item['fields']['name'].replace('\"', '')[:50]
                print('succes')
            if 'description' in item['fields']:
                item['fields']['description'] = item['fields']['description'].replace('\"', '')[:200]
            if 'slug' in item['fields']:
                item['fields']['slug'] = item['fields']['slug'][:197]
                # Ajouter un nombre aléatoire de 3 chiffres à la fin du slug
                item['fields']['slug'] += f'{random.randint(100, 999)}'    
        
        # Sauvegarder le fichier JSON formaté
        with open('ProdDatabases/products_data_format.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except ImportError as exc:
        print(exc)
        sys.exit(1)        


if __name__ == '__main__':
    main()    
