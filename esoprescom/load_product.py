# myapp/management/commands/load_products.py

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json
import django
import random
from django.core.files import File
from django.core.management.base import BaseCommand

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    try:
        from apps.shop.models import Product, Category, Image
        categories = list(Category.objects.all())
        print(f"Categogy: {categories}")
        if not categories:
            print(f"No categories found. Please create some categories first.")
            return

        desktop_images_path = 'static/assets/images/Soprescom/desktop'
        laptop_images_path = 'static/assets/images/Soprescom/laptop'
        server_images_path = 'static/assets/images/Soprescom/server'
        onduleur_images_path = 'static/assets/images/Soprescom/onduleur'
        autre_images_path = 'static/assets/images/Soprescom/accessoire'

        desktop_images = [os.path.join(desktop_images_path, img) for img in os.listdir(desktop_images_path)]
        laptop_images = [os.path.join(laptop_images_path, img) for img in os.listdir(laptop_images_path)]
        server_images = [os.path.join(server_images_path, img) for img in os.listdir(server_images_path)]
        onduleur_images = [os.path.join(onduleur_images_path, img) for img in os.listdir(onduleur_images_path)]
        autre_images = [os.path.join(autre_images_path, img) for img in os.listdir(autre_images_path)]
        
        for i in range(100):
            solde_price = round(random.uniform(350000, 500000), 2)
            regular_price = solde_price + random.uniform(50000, 100000)
            product = Product(
                name=f'Product {i}',
                slug=f'product-{i}',
                description=f'This is a description of product {i}.',
                more_description=f'More description about product {i}.',
                additional_infos=f'Additional infos about product {i}.',
                solde_price = solde_price,
                regular_price = regular_price,
                brand=f'Brand {i % 10}',
                is_available=bool(random.getrandbits(1)),
                is_best_seller=bool(random.getrandbits(1)),
                is_new_arrival=bool(random.getrandbits(1)),
                is_featured=bool(random.getrandbits(1)),
                is_special_offer=bool(random.getrandbits(1)),
            )
            product.save()
            # Assign random categories to the product
            #assigned_categories = random.sample(categories, random.randint(1, len(categories)))
            #product.categories.set(assigned_categories)
            assigned_category = random.choice(categories)
            product.categories.add(assigned_category)  
            product.save()

            # Add images based on categories
            #for category in assigned_category:
            if 'desktop' in assigned_category.name.lower():
                chosen_images = random.sample(desktop_images, min(4, len(desktop_images)))
            elif 'laptop' in assigned_category.name.lower():
                chosen_images = random.sample(laptop_images, min(4, len(laptop_images)))
            elif 'server' in assigned_category.name.lower():
                chosen_images = random.sample(server_images, min(4, len(server_images)))
            elif 'onduleur' in assigned_category.name.lower():
                chosen_images = random.sample(onduleur_images, min(4, len(onduleur_images)))
            elif 'autre' in assigned_category.name.lower():
                chosen_images = random.sample(autre_images, min(4, len(autre_images)))            
            else:
                chosen_images = []

            for image_path in chosen_images:
                with open(image_path, 'rb') as image_file:
                    image_instance = Image(
                        product=product,
                        image=File(image_file, name=os.path.basename(image_path))
                     )
                    image_instance.save()

            print(f'Product {i} created with images.')

    except ImportError as exc:
        print(exc)
        sys.ecit(1)

if __name__ == '__main__':
    main()