from django.shortcuts import render, redirect
from apps.shop.models.Product import Stock


def sortie_journalier(request):
    
    # sorties = []
    # stocks = Stock.objects.all()
    # print('stocks:',stocks)
    # for stock in stocks:
    #     # Récupérer les CommandeArticle correspondants au produit du stock
    #     commande_articles = CommandeArticle.objects.filter(stock=stock)
        
    #     for commande_article in commande_articles:
    #         # Vérifier si cette CommandeArticle correspond à une sortie de stock
    #         if commande_article.quantite > 0:
    #             sortie = {
    #                 'client': commande_article.commande.client,
    #                 'produit': stock.produit,
    #                 'quantite_sortie': commande_article.quantite,
    #                 'date_commande': commande_article.commande.date_commande,
    #                 'stock_restant': stock.quantite - commande_article.quantite
    #             }
    #             sorties.append(sortie)
    
    context = {
        # 'sorties': sorties,
        'page':'stock',
        'subpage':'journalier_tab',
    }
    return render(request, 'servicedsi/index.html', context)