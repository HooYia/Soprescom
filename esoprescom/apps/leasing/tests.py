from leasing.factories import ClientleasingFactory, ListeimprimanteFactory
from leasing.models import Clientleasing, Listeimprimante, Consommable, Deploiement, Exploitation
import random
from datetime  import timezone,timedelta,datetime
from django.contrib.auth import get_user_model
from django.utils import timezone
#from datetime  import timezone,timedelta,datetime
from django.core import mail
from django.test import TestCase
from django.core.mail import EmailMessage


User = get_user_model()
current_time = timezone.now()

###### Phase 1 creation des users et des imprimantes
#for _ in range(10):
#    ClientleasingFactory.create()
#for _ in range(150):    
#    ListeimprimanteFactory.create()

 ### Ne pas commenter pour la suite
users = User.objects.all()


from django.core.mail import send_mail

class EmailTestCase(TestCase):

    def test_email_sent(self):
        # Création d'une instance de Sav_request (ou utilisez une déjà existante)
        sav_request = Sav_request.objects.create(
            type_sav='DEVEA',
            numero_dossier='12345',
            marque='My Marque',
            client_sav='My Client',
            resp_sav='My Resp',
            # Autres champs nécessaires
        )

        # Envoyer l'e-mail (comme il est configuré pour la console, il ne sera pas réellement envoyé)
        send_email_on_sav_request_created(sender=None, instance=sav_request, created=True)

        # Vérifier que l'e-mail a été envoyé
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Nouvelle requête SAV créée')
        self.assertIn('Une nouvelle requête SAV a été créée avec le numéro de dossier : 12345', mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].from_email, 'your@email.com')
        self.assertEqual(mail.outbox[0].to, ['recipient1@email.com', 'recipient2@email.com'])

        # Vous pouvez également vérifier d'autres détails de l'e-mail si nécessaire

#####################  1 deploiement
##### créer 50 instances de la classe Deploiement

#clients = Clientleasing.objects.all()
#imprimantes = Listeimprimante.objects.all()
#
#deploiements = []
#for i in range(150):
#    deploiement = Deploiement(
#        site= 'Site {}'.format(random.randint(1,20)),
#        adresseip=f'192.168.1.{i+1}',
#        date_deploiement=f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
#        listeimprimante=imprimantes[i],
#        clientleasing=random.choice(clients),  #[random.randint(1,9)],
#        userLog=random.choice(users)
#    )
#    deploiements.append(deploiement)
#Deploiement.objects.bulk_create(deploiements)

#########     Phase 3 -- Consommable
#### Liste de références et désignations aléatoires
#references = ['REF-{}'.format(i) for i in range(1, 20)]
#designations = ['Consommable {}'.format(i) for i in range(1, 20)]
#####print(users)
##### Création de 200 instances de Consommable
#for i in range(1, 20):
#    consommable = Consommable()
#    consommable.bordereausortie = 'BS-{}'.format(random.randint(1,20))
#    consommable.type = random.choice([choice[0] for choice in Consommable.TypeConsommable.choices])
#    consommable.reference = references[i-1]
#    consommable.designation = designations[i-1]
#    consommable.description = 'Description pour Consommable {}'.format(i)
#    consommable.typeproduit = random.choice([choice[0] for choice in Consommable.OrigineConsommable.choices])
#    consommable.quantite = random.randint(50, 500)
#    consommable.userLog = random.choice(users)
#    consommable.date = current_time
#    consommable.save()



    
#################  3 Exploitation

# Récupérer tous les utilisateurs existants
#users = User.objects.all()
'''
#### Liste de types d'interventions possibles
type_interventions = [choice[0] for choice in Exploitation.Typeintervention.choices]
# Récupérer toutes les instances de Deploiement et Consommable existantes
deploiements = Deploiement.objects.all()
consommables = Consommable.objects.all()

# Créer 200 instances de la classe Exploitation
for i in range(200):
    # Choix aléatoire d'un Deploiement et d'un Consommable existants
    intervention = random.choice(type_interventions)
    deploiement = random.choice(deploiements)
    consommable = random.choice(consommables)
    
    # Création d'une instance de la classe Exploitation
    if (intervention =="Remplacement consommable"):
        qt=random.randint(1, 10)
        toner=0
        old_index=0
        new_index=0
    elif (intervention =="Releve fin du mois"):
        qt=0
        toner=f"{random.randint(0, 80)}%"
        old_index=random.randint(1000, 50000)
        new_index= old_index + random.randint(500, 9999)
    else:
        qt=random.randint(10, 50)
        toner=0
        old_index=0
        new_index=0
    exploitation = Exploitation.objects.create(
        intervention=intervention,
        deploiement=deploiement,
        quantite=qt,
        pourcentage_toner=toner,
        ancien_index = old_index,
        nouvel_index= new_index,
        description=f"Description de l'intervention {i+1}",
        userLog=random.choice(users)
        )

    # Ajout du consommable à l'instance de la classe Exploitation créée
    exploitation.consommable.add(consommable)

    # Modification de la date de l'intervention aléatoirement
    # Modification de la date de l'intervention aléatoirement
    date_min = datetime(2023, 1, 1)
    date_max = datetime(2023, 5, 28)

    delta = date_max - date_min
    random_date = date_min + timedelta(days=random.randint(0, delta.days), seconds=random.randint(0, delta.seconds))
    date = random_date    
    exploitation.date = random_date
    exploitation.save()
'''