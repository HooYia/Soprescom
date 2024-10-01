# myapp/management/commands/load_products.py

import os,sys
import random
from django.core.management.base import BaseCommand
from django.core.files import File
import django
import pandas as pd



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    # Lire le fichier Excel
    file_path = 'InputFiles/ORDINATEUR_PORTABLE_DISPO.xlsx'
    print('file_path:',file_path)
    df = pd.read_excel(file_path, header=0)  # Ignore la première ligne
    print('df:',df)
    # Afficher les colonnes pour vérifier leurs noms
    references = df['reference']
    designation = df['designation']
    
    try:
        from apps.shop.models import Product, Category, Image
        from apps.shop.models.Product import Product, Stock
        from load_task_in_production import search_images,search_serpapi_images, download_image,save_images_for_product
        categories = list(Category.objects.all())
        #if not categories:
        #    print(f"No categories found. Please create some categories first.")
        #    return
        #Parcourir les lignes du fichier et créer des produits
        for index, row in df.iterrows():
            prix_unitaire_str = str(row['prix_unitaire']).replace(' ', '').replace('\xa0', '')
            prix_unitaire_float = float(prix_unitaire_str) if prix_unitaire_str != '' else 0
            # Utilisation des variables dans le dictionnaire
            regular_price = prix_unitaire_float
            print('prix_unitaire_float:',prix_unitaire_float)
            solde_price = prix_unitaire_float * 0.96

            insert_row = {
                'reference' :  row['reference'],
                'name' :  row['designation'],
                'description' :  f"{row['designation']} ({row['quantite']} unités disponibles.)",
                'additional_infos' :'',
                'price' :  prix_unitaire_float,
                'category_name' :  row['categorie'],
                'spec_link' :  'https://exemple.com/fiche_technique',
                'quantite' :  row['quantite'],
                'regular_price' :  regular_price,
                'solde_price' :solde_price,
                'brand' : f'Brand ',
                'is_available' : bool(random.getrandbits(1)),
                'is_best_seller' : bool(random.getrandbits(1)),
                'is_new_arrival' : bool(random.getrandbits(1)),
                'is_featured' : bool(random.getrandbits(1)),
                'is_special_offer' : bool(random.getrandbits(1)),
                }
            print('insert_row:',insert_row['category_name'])
            # Associer la catégorie
            try:
                category, created = Category.objects.get_or_create(name=insert_row['category_name'])
                
                product, created = Product.objects.get_or_create(
                    name=insert_row['name'],  description=insert_row['description'],
                    more_description = '', additional_infos ='',
                    regular_price = insert_row['regular_price'] , solde_price = insert_row['solde_price'],
                    brand = insert_row['brand'],
                    is_available =insert_row['is_available'], is_best_seller =insert_row['is_best_seller'],
                    is_new_arrival =insert_row['is_new_arrival'], is_featured =insert_row['is_featured'],
                    is_special_offer =insert_row['is_special_offer'])
                product.categories.add(category)
                if created: # Nouvelle creation => ajout stock
                    Stock_instance = Stock(stock_produit=product)
                    Stock_instance.quantite = int(insert_row['quantite'])
                    Stock_instance.save()
                else: # Produit existe  => update stock
                    Stock_instance = Stock(stock_produit=product)
                    Stock_instance.quantite += int(insert_row['quantite'])
                    Stock_instance.save()
                reference = insert_row['reference']
                designation = insert_row['name']
                #image_urls = search_google_info(reference)
                result = search_serpapi_images(reference,designation)
                #get Image url and link information for product
                images_url = result['images_url']
                product.additional_infos = result['more_detail']
                product.save()
                if result['images_url']:
                    save_images_for_product(product, result['images_url'], reference)
                 
            except  Exception as e:
                print('e:',e)
            
    except ImportError as exc:
        print(exc)
        sys.exit(1)

if __name__ == '__main__':
    main()    

