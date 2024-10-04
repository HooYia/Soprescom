
import os
from googleapiclient.discovery import build
import pandas as pd
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from apps.shop.models import Product, Category, Image
# from serpapi import GoogleSearch

def search_google_info(reference):
        """Utilise l'API Google pour rechercher la date de fin de garantie et l'image."""
        api_key = 'AIzaSyCHm-Y_stQ7v7hqO40pAagZ_kHdvmCkh7Q'  # Clé API Google
        cse_id = '5744104a0b81e46cb'  # ID du moteur de recherche personnalisé
        service = build("customsearch", "v1", developerKey=api_key)
        query = f"{reference} "
        try:
            res = service.cse().list(q=query, cx=cse_id).execute()
            print('Res:',res)
            items = res.get('items', [])
            for item in items:
                # Logique pour extraire les informations d'intérêt
                #print('item:',item)
                end_of_warranty=''
                image_url=None
                link=item['link']
                titre=item['title']
                if 'warranty' in item['snippet'].lower():
                    end_of_warranty = "logique pour extraire la date de fin de garantie"
                if 'pagemap' in item and 'cse_image' in item['pagemap']:
                    image_url = item['pagemap']['cse_image'][0]['src']
                return {
                        'end_of_warranty': end_of_warranty,
                        'image_url': image_url,
                        'link':link,
                        'titre': titre
                    }
                print('image_url:',image_url)
        except Exception as e:
            print(f"Erreur lors de la recherche Google: {e}")
        return None

# Fonction pour rechercher des images Google
def search_images(reference,designation):
    search_url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        'q': f"{reference}  {designation}",
        'cx': '5744104a0b81e46cb',
        'key': 'AIzaSyCHm-Y_stQ7v7hqO40pAagZ_kHdvmCkh7Q',
        'searchType': 'image',
        'num': 4,  # Obtenir 4 images
        #'imgSize': 'medium',  # Taille de l'image
        #'safe': 'on'  # Vous pouvez mettre 'on' pour filtrer le contenu inapproprié
    }

    response = requests.get(search_url, params=params)
    data = response.json()
    print('data:',data)
    results = {
        'images_url': [],
        'more_detail': None,
        'title': None
    }
    
    if 'items' in data and len(data['items']) > 0:
        # Récupérer les 4 images
        for item in data['items']:
            results['images_url'].append(item['link'])

        # Prendre uniquement le premier élément pour le lien contextuel et le titre
        first_item = data['items'][0]
             
        # Récupérer le 'contextLink' (lien contextuel) et le 'title'
        if 'image' in first_item:
            results['more_detail'] = first_item['image'].get('contextLink')
        if 'kind' in first_item:
            results['title'] = first_item['title']
    print('results:',results)    
    return results



def search_serpapi_images(reference,designation):
    params1 = {
        "engine": "google",
        "q": reference,
        #"ll": "@40.7455096,-74.0083012,15.1z",
        "num": "4",
        "type": "search",
        "api_key": "df95d8db357af8f9d090b079b80ed0af7b6694a5f19ec8df8809d01d3f316fe6"
        }
    params2 = {
        "engine": "google_images",  # Utiliser l'engin Google Images
        "q": f"{reference} {designation}",
        "num": "4",  # Obtenir 4 résultats
        "api_key": "df95d8db357af8f9d090b079b80ed0af7b6694a5f19ec8df8809d01d3f316fe6"
    }
  
    search = " " #GoogleSearch(params2)
    data = search.get_dict()
    results = {
        'images_url': [],
        'more_detail': None,
        'title': None
    }
    #if "images_results" in results:
    if 'images_results' in data and len(data['images_results']) > 0:
        
        for result in data["images_results"][:4]:  # Limiter à 4 images
            results['images_url'].append(result["original"])  # Utiliser l'URL de l'image originale
        #print('results[images_url]',results['images_url'])
        # Prendre uniquement le premier élément pour le lien contextuel et le titre
        first_item = data['images_results'][0]    
        #print('first_item:',first_item)
        if 'title' in first_item:
            results['title'] = first_item['title']   #.get('contextLink')
        if 'link' in first_item:
            results['more_detail'] = first_item['link']  #.get('contextLink')
    
    #print('results:', results)
    return results

# Fonction pour télécharger l'image
def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        #img_temp = NamedTemporaryFile(delete=True)
        # Supprimer delete=True
        img_temp = NamedTemporaryFile()  
        img_temp.write(response.content)
        img_temp.flush()
        return img_temp
    return None
   

# Fonction pour enregistrer les images dans le modèle `Image`
def save_images_for_product(product, images_url, reference):
    for i, image_url in enumerate(images_url):
        # Télécharger l'image depuis l'URL
        try:
            #img_temp = download_image(image_url, f'{reference}_img{i+1}.jpg')
            img_temp = download_image(image_url)
            print('img_temp:',img_temp)
            # Créer une instance de l'image liée au produit
            image_instance = Image(product=product)
            
            # Sauvegarder l'image dans la table `Image`
            image_instance.image.save(f'{reference}_img{i+1}.jpg', File(img_temp))
            # Sauvegarder l'instance dans la base de données
            image_instance.save()
            
            print('Insert image succes')
        except Exception as e:
            print('Exception:',e)
                



# Fonction pour créer un produit avec ses images
def create_product_with_images(row):
    reference = row['reference']
    name = row['designation']
    description = f"{name} {row['Quantite']} unités disponibles."
    price = row['prix_unitaire']
    category_name = row['categorie']
    spec_link = 'https://exemple.com/fiche_technique'

    # Associer la catégorie
    category, created = Category.objects.get_or_create(name=category_name, slug=category_name.lower())

    # Créer ou obtenir le produit
    product, created = Product.objects.get_or_create(name=name, slug=reference.lower(), description=description, solde_price=price)
    product.categories.add(category)

    # Rechercher les images
    image_urls = search_images(reference)
    if image_urls:
        for i, image_url in enumerate(image_urls):
            img_temp = download_image(image_url, f'{reference}_img{i+1}.jpg')
            product_image_field = f'image_{i+1}'
            getattr(product, product_image_field).save(f'{reference}_img{i+1}.jpg', File(img_temp))

    # Sauvegarder le produit
    product.save()

