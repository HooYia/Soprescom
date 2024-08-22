# myapp/management/commands/load_products.py

import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.shop.models import Product, Category, Image
import django

class Command(BaseCommand):
    help = 'Load 100 products into the database'
    django.setup()
    def handle(self, *args, **kwargs):
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR('No categories found. Please create some categories first.'))
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
            product = Product(
                name=f'Product {i}',
                slug=f'product-{i}',
                description=f'This is a description of product {i}.',
                more_description=f'More description about product {i}.',
                additional_infos=f'Additional infos about product {i}.',
                stock=random.randint(1, 100),
                solde_price=round(random.uniform(10.0, 100.0), 2),
                regular_price=round(random.uniform(10.0, 100.0), 2),
                brand=f'Brand {i % 10}',
                is_available=bool(random.getrandbits(1)),
                is_best_seller=bool(random.getrandbits(1)),
                is_new_arrival=bool(random.getrandbits(1)),
                is_featured=bool(random.getrandbits(1)),
                is_special_offer=bool(random.getrandbits(1)),
            )
            product.save()
            # Assign random categories to the product
            assigned_categories = random.sample(categories, random.randint(1, len(categories)))
            product.categories.set(assigned_categories)
            product.save()

            # Add images based on categories
            for category in assigned_categories:
                if 'desktop' in category.name.lower():
                    chosen_images = random.sample(desktop_images, random.randint(1, len(desktop_images)))
                elif 'laptop' in category.name.lower():
                    chosen_images = random.sample(laptop_images, random.randint(1, len(laptop_images)))
                elif 'server' in category.name.lower():
                    chosen_images = random.sample(server_images, random.randint(1, len(laptop_images)))
                elif 'onduleur' in category.name.lower():
                    chosen_images = random.sample(onduleur_images, random.randint(1, len(laptop_images)))
                elif 'autre' in category.name.lower():
                    chosen_images = random.sample(autre_images, random.randint(1, len(laptop_images)))            
                else:
                    chosen_images = []

                for image_path in chosen_images:
                    with open(image_path, 'rb') as image_file:
                        image_instance = Image(
                            product=product,
                            image=File(image_file, name=os.path.basename(image_path))
                        )
                        image_instance.save()

            self.stdout.write(self.style.SUCCESS(f'Product {i} created with images.'))

