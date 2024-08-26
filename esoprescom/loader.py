#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json
import django

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    try:
        from apps.shop.models import Category, Collection, Slider, \
            Carrier, Image,NavCollection, Page, Setting, Social
        files_path = [
            'databases/shop_carrier.json',
            'databases/shop_category.json',
            'databases/shop_collection.json',
            'databases/shop_page.json',
            'databases/shop_navcollection.json',
            # 'databases/shop_image.json',
            'databases/shop_product_categories.json',
            'databases/shop_product.json',
            'databases/shop_setting.json',
            'databases/shop_slider.json',
            'databases/shop_social.json',
        ]
        models = {
            'shop_carrier': Carrier,
            'shop_category': Category,
            'shop_image': Image,
            'shop_navcollection':NavCollection,
            'shop_page':Page,
            'shop_setting': Setting,
            'shop_slider': Slider,
            'shop_social':Social,
            'shop_collection': Collection
           
        }
        for file_path in files_path:
            with open(file_path,'r') as file:
                entity = file_path.split('/')[1].split('.')[0]
                print(f"entity '{entity}'")     
                model = models.get(entity)
                print(f"Model '{model}'")     
                if model:
                    data = json.load(file)
                    for item in data:
                        #header = item.get('header')
                        #row = item.get('row')
                        del item['id']
                        print(f"entity_data '{item}'.")    
                        model.objects.create(**item)
                else:
                    print(f"Model '{entity}' not found.")           
    except ImportError as exc:
        print(exc)
        sys.exit(1)
    


if __name__ == '__main__':
    main()
