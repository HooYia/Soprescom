import os
from googleapiclient.discovery import build
import requests

def search_google_info(reference,designation):
        """Utilise l'API Google pour rechercher la date de fin de garantie et l'image."""
        #api_key = os.getenv('AIzaSyBaVCxR04xT9Si06o7x7g09DfyseFzUQEI')  # Clé API Google
        #cse_id = os.getenv('5744104a0b81e46cb')  # ID du moteur de recherche personnalisé
        api_key = 'AIzaSyC_R0BcteLidkinIrNqMHOjjoPgv1nhJro'  # Clé API Google
        cse_id = '5744104a0b81e46cb'  # ID du moteur de recherche personnalisé
        service = build("customsearch", "v1", developerKey=api_key)
        query = f"{reference} {designation}"
        try:
            res = service.cse().list(q=query, cx=cse_id).execute()
            #print('Res:',res)
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