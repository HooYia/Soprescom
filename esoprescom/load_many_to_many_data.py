import os,sys
from django.core.management.base import BaseCommand
from django.core.files import File
import django

import json


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    try:
        from apps.shop.models import Product, Category
        # Accéder à toutes les relations Product <-> Category
        relations = []
        for product in Product.objects.all():
            categories = product.categories.all()
            for category in categories:
                relations.append({
                    'product_id': product.id,
                    'category_id': category.id
                })

        # Exporter les relations dans un fichier JSON
        import json
        with open('ProdDatabases/product_category_relations.json', 'w') as f:
            json.dump(relations, f, indent=4)
    except ImportError as exc:
        print(f"ImportError: {exc}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)      


if __name__ == '__main__':
    main()    
        
