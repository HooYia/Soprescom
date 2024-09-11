from django.db import models
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import django.db
import requests
#from django.utils.translation import gettext as _  ugettext_lazy 
from django.utils.translation import gettext_lazy as _  
from django.contrib.auth import get_user_model
from datetime import datetime,timedelta,date
from django.db.models import Count,Sum, Case, When, Sum
from django.core.exceptions import ObjectDoesNotExist
from urllib.parse import urlencode
from django.core.files.base import ContentFile
from django.utils.timezone import now
from googleapiclient.discovery import build
from django.utils import timezone
from django.core.validators import MaxLengthValidator
from apps.serviceapresvente.models.tasks import Send_Email,send_email_with_template, \
                                                send_email_with_template_customer, \
                                                send_instance_email_with_template_task, \
                                                send_email_with_template_task


from apps.accounts.models.Customer import Customer

User = get_user_model()

   
## Gestion Client 
class Clientleasing(models.Model):
    idclientleasing = models.BigAutoField(primary_key=True)
    nom = models.CharField( max_length=50,unique=True, null=False, blank=False,verbose_name =_('Nom'),db_index=True) 
    adresse = models.CharField(verbose_name =_('Adresse'),max_length=100,null=False, blank=False)
    contact = models.CharField(verbose_name =_('Contact'),max_length=50,null=False, blank=False)
    localite = models.CharField(verbose_name =_('Région'),max_length=50, null=False, blank=False)
    refcontrat = models.CharField(verbose_name =_('N° Contrat '),unique=True, max_length=45, null=False, blank=False)
    duree_contrat = models.CharField(verbose_name =_('Durée Contrat '), max_length=10, null=False, blank=False)
    email  = models.EmailField(verbose_name =_('Email'),max_length=50,blank=True, null=True)
    date = models.DateField(verbose_name =_('Date Contrat'),blank=True, null=True)
    #userLog = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    #def get_string_fields(self):
    #   return '%(name)s - %(addresse)s - %(contact)s - %(localite)s - %(refcontrat)s  -  \
    #                %(email)s - %(date)s' % { 'name': self.name, 'addresse': self.addresse, 
    #        'contact': self.contact, 'localite': self.localite, 'refcontrat': self.refcontrat,
    #        'email': self.email,  'date': self.date}
    

   #auteur =models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    class Meta:
      #app_label = 'leasing'  
      db_table = 'leasing_clientleasing'
      managed = True
      verbose_name = 'Clientleasing'
      verbose_name_plural = 'Clientleasings'
      ordering = ["nom"]
    
    def __str__(self) -> str:
      return self.nom

    @classmethod
    def select_data(cls):
        queryset = Clientleasing.objects.annotate(num_deploiements=models.Count('deploiement__clientleasing')).order_by('nom', 'num_deploiements')
        return queryset
    
##Gestion Imprimante
class Listeimprimante(models.Model):
    class ETATIMPRIMANTE(models.TextChoices):
          OK ="ETAT CORRECT","ETAT CORRECT"
          DEGRADE ="ETAT Dégradé","ETAT Dégradé"
          NONOK ="Non fonctionnel","Non fonctionnel"
    idlisteimprimante = models.BigAutoField(primary_key=True)
    numero_serie = models.CharField(verbose_name =_('Numero Série'),unique=True,max_length=50)
    reference = models.CharField(verbose_name =_('Référence'),max_length=50,null=False, blank=False,db_index=True)
    designation = models.CharField(verbose_name =_('Désignation'),max_length=50,null=False, blank=False,db_index=True)
    description = models.CharField(verbose_name =_('Description'),max_length=50,blank=True, null=True)
    date_acquisition = models.DateField(verbose_name =_('Date Acquisition'), blank=True, null=True)
    garantie = models.CharField(max_length=10,verbose_name =_('Garantie'), blank=True, null=True)
    endoflife = models.DateField(verbose_name =_('End of Life'), blank=True, null=True)
    image = models.ImageField(upload_to='leasing/', null=True, blank=True)
    flag = models.BooleanField(default=False)
    ## Fiel dpour la maintenance
    niveau_toner = models.CharField(max_length=5, verbose_name=_('Toner (%)'), blank=True, null=True)
    niveau_photoconducteur = models.CharField(max_length=5, verbose_name=_('Toner (%)'), blank=True, null=True)
    niveau_hit_maintenance = models.CharField(max_length=5, verbose_name=_('Toner (%)'), blank=True, null=True)
    ancien_index = models.IntegerField(blank=True, null=True)
    nouvel_index = models.IntegerField(blank=True, null=True)
    moyenne_impression =models.FloatField(blank=True, null=True)
    etat = models.CharField(max_length=15, verbose_name=_('Intervention'), choices=ETATIMPRIMANTE.choices, default=ETATIMPRIMANTE.OK)
    
    class Meta:
        managed = True
        db_table = 'leasing_listeimprimante'
        verbose_name = 'listeimprimante'
        verbose_name_plural = 'listeimprimantes'
       
    
    def __str__(self) -> str:
      return "{}".format(self.reference)
    
    def maintenance_due(self):
        derniere_maintenance = Maintenance.objects.filter(imprimante=self).order_by('-date_maintenance').first()
        if derniere_maintenance and derniere_maintenance.prochaine_maintenance <= timezone.now().date():
            return True
        return False

    
    def save(self, *args, **kwargs):
        # Appel à l'API Google pour récupérer les informations si elles ne sont pas fournies
        if not self.endoflife or not self.image:
            search_results = self.search_google_info()
            if search_results:
                self.endoflife = search_results.get('end_of_warranty')
                self.image = search_results.get('image_url')
        super().save(*args, **kwargs)

    def search_google_info(self):
        """Utilise l'API Google pour rechercher la date de fin de garantie et l'image."""
        api_key = os.getenv('AIzaSyBoAi6Jr6zeiklXsybwEjQjjIecJB6_gac')  # Clé API Google
        cse_id = os.getenv('gen-lang-client-0767018349')  # ID du moteur de recherche personnalisé

        service = build("customsearch", "v1", developerKey=api_key)
        query = f"{self.reference} {self.designation} {self.numero_serie}"

        try:
            res = service.cse().list(q=query, cx=cse_id).execute()
            items = res.get('items', [])
            for item in items:
                # Logique pour extraire les informations d'intérêt
                if 'warranty' in item['snippet'].lower():
                    end_of_warranty = "logique pour extraire la date de fin de garantie"
                if 'pagemap' in item and 'cse_image' in item['pagemap']:
                    image_url = item['pagemap']['cse_image'][0]['src']
                    return {
                        'end_of_warranty': end_of_warranty,
                        'image_url': image_url
                    }
        except Exception as e:
            print(f"Erreur lors de la recherche Google: {e}")
        return None
    
    @classmethod
    def LeasingStatImprimante(cls): 
        queryset_countAll = Listeimprimante.objects.count() 
        queryset_RefAgg = Listeimprimante.objects.values(
            'reference').annotate(
                status_count=Count('reference')).order_by('reference') 
        queryset_ImpStatus = Listeimprimante.objects.values('flag').annotate(
                status_count=Count('flag')).order_by('flag')    
        queryset_Refstatus = Listeimprimante.objects.values('reference','flag').annotate(
                status_count=Count('reference')).order_by('reference')    
        
        return queryset_countAll,queryset_RefAgg,queryset_ImpStatus,queryset_Refstatus
    


## Deploiement sur site
class Deploiement(models.Model):
    iddeploiement = models.BigAutoField(primary_key=True)
    clientleasing = models.ForeignKey(Clientleasing,on_delete=models.SET_NULL,null=True)
    site = models.CharField(verbose_name =_('Site'),max_length=50,null=False, blank=False,db_index=True)
    adresseip = models.CharField(verbose_name =_('Adresse IP'),max_length=50,null=True, blank=True)
    date_deploiement = models.DateField(verbose_name =_('Date Deploiement'),blank=True, null=True)
    listeimprimante = models.OneToOneField(Listeimprimante,  on_delete=models.SET_NULL,null=True)
    #userLog = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
 
    class Meta:
        managed = True
        db_table = 'leasing_deploiement'
        verbose_name = 'deploiement'
        verbose_name_plural = 'deploiements'
        ordering = ["iddeploiement"]
    
    def __str__(self):
        return "{}-{}-{} ({})".format(self.clientleasing,self.site,self.listeimprimante,self.adresseip)
    @property
    def listeimprimante_free(self):
        return self.get_liste_imprimantes()

    def get_liste_imprimantes(self):
        # Récupérer l'imprimante liée à ce déploiement avec flag=0 s'il existe
        if self.listeimprimante and not self.listeimprimante.flag:
            return self.listeimprimante
        return None
    
    @classmethod
    def select_data(cls):
        queryset = Deploiement.objects.values('clientleasing__nom', 'site').annotate(num_deploiements=models.Count('site')).order_by('clientleasing__nom', 'site')
        return queryset
    ##Obtenir le nombre d'imprimante par Client
    @classmethod
    def select_Nbre_Client_Impr(cls):
        queryset = Deploiement.objects.values('clientleasing__nom').annotate(nombreImprimante=models.Count('listeimprimante__reference')).order_by('clientleasing__nom')
        return queryset

### Gestion Consommable
class Consommable(models.Model):
    class TYPE_MODELE(models.TextChoices):
          HP ="HP","HP"
          LEXMARK ="LEXMARK","LEXMARK"
          CANON ="Canon","Canon"
          AUTRE ="AUTRE","AUTRE"

    class TYPE_PRODUIT(models.TextChoices):
          TONER ="Toner","Toner"
          TAMBOUR ="Tambour","Tambour"
          KIT_MAINTENANCE ="Kit de Maintenance","Kit de Maintenance"
          PAPIER ="Papier RAM","Papier RAM"
          FUSER="Fuser","Fuser"
          FIMLFOUR="Flim Four","Flim Four"

    idconsommable = models.BigAutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    bordereausortie = models.CharField(verbose_name =_('Bordereau SOP'), max_length=30,null=False, blank=False)
    marque = models.CharField(max_length=10, choices=TYPE_MODELE, default=TYPE_MODELE.LEXMARK,verbose_name=_('Marque'), null=False, blank=False)
    # Associer au modèle d'imprimante
    modeleimprimante = models.CharField(max_length=15, verbose_name=_('Modele Imprimante'), null=False, blank=False,default='')
    
    produit = models.CharField(max_length=20, choices=TYPE_PRODUIT,default=TYPE_PRODUIT.TONER, verbose_name=_('Produit'), null=False, blank=False)
    reference = models.CharField(verbose_name =_('Référence'),unique=True, max_length=30,null=False, blank=False,db_index=True)
    designation = models.CharField(verbose_name =_('Désignation'),unique=True,max_length=50,null=False, blank=False)
    description = models.CharField(verbose_name =_('Description'),max_length=100,null=True, blank=True)
    quantite = models.IntegerField(verbose_name =_('Quantité'),default=0,null=False, blank=False)
    seuilLimite = models.IntegerField(verbose_name =_('Seuil'),default=5,null=False, blank=False)
    image = models.ImageField(upload_to='leasing/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta: 
        managed = True
        db_table = 'leasing_consommable'
        verbose_name = 'Consommable'
        verbose_name_plural = 'Consommables'
        
    
    def __str__(self) -> str:
       return "{}".format(self.idconsommable)
       #return "{} - {} - {}".format(self.type,self.reference,self.quantite)

    @classmethod
    def select_conso_stock(cls):
        queryset = Consommable.objects.values('modeleimprimante','produit','reference','seuilLimite').annotate(stock=Sum('quantite')).order_by('modeleimprimante','produit','reference')
        return queryset

### Exploitation d'une imprimante
class ConsommableExploitation(models.Model):
    id = models.BigAutoField(primary_key=True)
    exploitation = models.ForeignKey('Exploitation', on_delete=models.CASCADE)
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE)
    quantite = models.IntegerField(verbose_name=_('Quantité'), default=0)

    class Meta:
        unique_together = ('exploitation', 'consommable')

class Exploitation(models.Model):
    class Typeintervention(models.TextChoices):
          remplacement ="Remplacement consommable","Remplacement consommable"
          releve = "Releve fin du mois","Releve fin du mois"
          papier = "Fourniture Carton Papier","Fourniture Carton Papier"
          maintennace = "Maintenance","Maintenance"
    class ETATIMPRIMANTE(models.TextChoices):
          OK ="ETAT CORRECT","ETAT CORRECT"
          DEGRADE ="ETAT Dégradé","ETAT Dégradé"
          NONOK ="Non fonctionnel","Non fonctionnel"
          
    idexploitation = models.BigAutoField(primary_key=True)
    date_exploitation = models.DateField(auto_now=True)
    intervention = models.CharField(max_length=30, verbose_name=_('Intervention'), choices=Typeintervention.choices, default=Typeintervention.papier)
    consommables = models.ManyToManyField(Consommable, through=ConsommableExploitation)
    deploiement = models.ForeignKey(Deploiement, on_delete=models.SET_NULL, null=True)
    niveau_toner = models.CharField(max_length=5, verbose_name=_('Toner (%)'), blank=True, null=True)
    niveau_photoconducteur = models.CharField(max_length=5, verbose_name=_('Toner (%)'), blank=True, null=True)
    niveau_hit_maintenance = models.CharField(max_length=5, verbose_name=_('Toner (%)'), blank=True, null=True)
    ancien_index = models.IntegerField(blank=True, null=True)
    nouvel_index = models.IntegerField(blank=True, null=True)
    moyenne_impression =models.FloatField(blank=True, null=True)
    etat = models.CharField(max_length=15, verbose_name=_('Intervention'), choices=ETATIMPRIMANTE.choices, default=ETATIMPRIMANTE.OK)
    observation = models.TextField(verbose_name =_('Observation'),max_length=100,null=False, blank=False)
    

"""
class Exploitation(models.Model):
    class Typeintervention(models.TextChoices):
          remplacement ="Remplacement consommable","Remplacement consommable"
          releve = "Releve fin du mois","Releve fin du mois"
          papier = "Fourniture Carton Papier","Fourniture Carton Papier"
          

    idexploitation = models.BigAutoField(primary_key=True)
    date_exploitation = models.DateField(auto_now=True)
    intervention = models.CharField(max_length=50,verbose_name =_('Intervention'),
                                    choices=Typeintervention.choices,default=Typeintervention.papier)
    consommable = models.ManyToManyField(Consommable)
    deploiement = models.ForeignKey(Deploiement, on_delete=models.SET_NULL,null=True)
                                    
    quantite = models.IntegerField(blank=True, null=True)
    pourcentage_toner = models.CharField(max_length=5,verbose_name =_('Toner (%) '),blank=True, null=True)
    ancien_index = models.IntegerField(blank=True, null=True)
    nouvel_index = models.IntegerField(blank=True, null=True)
    observation  = models.CharField(verbose_name =_('Description'),max_length=100,blank=False, null=False)
    userLog = models.ForeignKey(User, on_delete = models.SET_NULL, null=True,blank = True)
    

    class Meta:
        managed = True
        db_table = 'leasing_exploitation'
        verbose_name = 'Exploitation'
        verbose_name_plural = 'Exploitations'
        ordering = ["date_exploitation"]
    
    def __str__(self) -> str:
       #return "{} - {} - {} - {}".format(self.consommable.type,self.deploiement.site,self.deploiement.listeimprimante.reference,self.deploiement.clientleasing.nom)
       return "{}".format(self.idexploitation) #consommable.type,self.deploiement.site,self.deploiement.listeimprimante.reference)
"""

### Historique ajout consommable
class HistioriqueConsommable(models.Model):
    idhistconsommable = models.BigAutoField(primary_key=True)
    date = models.DateField(default=datetime.now)
    bordereausortie = models.CharField(verbose_name =_('Bordéreau de Sortie'), max_length=30,null=False, blank=False)
    reference = models.CharField(verbose_name =_('Référence'), max_length=30,null=False, blank=False,db_index=True)
    designation = models.CharField(verbose_name =_('Désignation'),max_length=50,null=False, blank=False)
    description = models.CharField(verbose_name =_('Description'),max_length=100,null=False, blank=False)
    typeproduit = models.CharField(verbose_name =_('Catégorie'),max_length = 100,null=False, blank=False)
    quantite = models.IntegerField(verbose_name =_('Quantité'),default=0,null=False, blank=False)
    action = models.CharField(verbose_name =_('Add_or_dell'),max_length = 100,null=False, blank=False)
    userLog = models.CharField(verbose_name =_('User_Id'),max_length = 100,null=False, blank=False)

    class Meta:
        managed = True
        db_table = 'leasing_histioriqueconsommable'
        verbose_name = 'Exploitation'
        verbose_name_plural = 'Exploitations'
        ordering = ["date"]
    

class GestionIncident(models.Model):
    class NATUREINCIDENT(models.TextChoices):
          INCIDENT_0 ="Défaut impression","Défaut impression"
          INCIDENT_1 ="Probleme Cartouche","Probleme Cartouche"
          INCIDENT_2 ="Défaut Alimentation","Défaut Alimentation"

    class STATUT(models.TextChoices):
          OK ="Résolu","Résolu"
          NON_OK ="Non résolu","Non résolu"
          
    idincident = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client_leasing = models.CharField(verbose_name =_('Leasing User'), max_length=30,null=False, blank=False, default='Leasing Team DSI')
    resp_dossier = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    deploiement = models.ForeignKey(Deploiement, on_delete=models.SET_NULL, null=True)
    incident = models.CharField(max_length=25, verbose_name=_('Type incident'), choices=NATUREINCIDENT.choices, default=NATUREINCIDENT.INCIDENT_0)
    statut = models.CharField(max_length=15, verbose_name=_('Statut incident'), choices=STATUT.choices, default=STATUT.NON_OK)
    observation = models.TextField(verbose_name =_('Observation'),null=True,blank=True,
                  validators=[MaxLengthValidator(limit_value=100)])

class Maintenance(models.Model):
    class STATUT(models.TextChoices):
          maintenance_0 ="OKAY","OKAY"
          maintenance_1 ="NON OK","NON OK"
          

    idmaintenance = models.BigAutoField(primary_key=True)
    imprimante = models.ForeignKey(Listeimprimante, on_delete=models.CASCADE)
    date_maintenance = models.DateField(auto_now_add=True)
    maintenue_par = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=15,  verbose_name=_('Statut'), choices=STATUT.choices, default=STATUT.maintenance_0)
    description = models.TextField(verbose_name=_('Description'), max_length=255, null=True, blank=True)
    prochaine_maintenance = models.DateField(verbose_name=_('Prochaine maintenance'), blank=True, null=True)

    class Meta:
        db_table = 'leasing_maintenance'
        verbose_name = 'Maintenance'
        verbose_name_plural = 'Maintenances'
        ordering = ['date_maintenance']

    def save(self, *args, **kwargs):
        if self.statut == self.STATUT.maintenance_0:  # Vérifie si le statut est "OKAY"
            if not self.prochaine_maintenance:
                # La prochaine maintenance est fixée automatiquement à 1 mois après la date de maintenance actuelle
                self.prochaine_maintenance = datetime.now().date() + timedelta(days=30)
        else:
            # Si le statut n'est pas "OKAY", on ne met pas à jour prochaine_maintenance
            self.prochaine_maintenance = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.imprimante.numero_serie} - {self.date_maintenance}"

"""

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

"""