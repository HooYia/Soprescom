from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import django.db
#from django.utils.translation import gettext as _  ugettext_lazy 
from django.utils.translation import gettext_lazy as _  
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models import Count,Sum, Case, When, Sum

User = get_user_model()

class typeCategorie(models.Model):
      idcategorie = models.BigAutoField(primary_key=True)
      categorie = models.CharField(verbose_name =_('Catégorie'), max_length=30,null=False, blank=False)
      class Meta: 
        managed = True
        db_table = 'Leasing_typeCategorie'
        ordering = ["categorie"]
      def __str__(self) -> str:
           return  f"{self.categorie}" 
    
      @staticmethod
      def get_categorieID_byName(categorie):
        return typeCategorie.objects.filter(categorie=categorie).values('idcategorie')
                              
class typeProduit(models.Model):
    idtypeproduit = models.BigAutoField(primary_key=True)
    categorie = models.ForeignKey(typeCategorie, on_delete=models.SET_NULL,null=True,db_index=True) 
    #departement  = models.CharField(verbose_name =_('Departement'), max_length=30,null=True, blank=True)
    designation  = models.CharField(verbose_name =_('Désignation'), max_length=30,null=True, blank=True)
    
    class Meta: 
        managed = True
        db_table = 'Leasing_typeProduit'
        ordering = ["designation"]
    def __str__(self) -> str:
       return  f"{self.designation}"    

    @staticmethod
    def get_typeProduit_byCategorieID(categorie_id):
        return typeProduit.objects.filter(categorie=categorie_id).values('idtypeproduit','designation')
## Gestion Client 
class Clientleasing(models.Model):
    idclientleasing = models.BigAutoField(primary_key=True)
    nom = models.CharField( max_length=50,unique=True, null=False, blank=False,verbose_name =_('Nom'),db_index=True) 
    adresse = models.CharField(verbose_name =_('Adresse'),max_length=100,null=False, blank=False)
    contact = models.CharField(verbose_name =_('Contact'),max_length=50,null=False, blank=False)
    localite = models.CharField(verbose_name =_('Région'),max_length=100, null=False, blank=False)
    refcontrat = models.CharField(verbose_name =_('N° Contrat '),unique=True, max_length=45, null=False, blank=False)
    email  = models.EmailField(verbose_name =_('Email'),max_length=50,blank=True, null=True)
    date = models.DateField(verbose_name =_('Date Contrat'),blank=True, null=True)
    userLog = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)

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
    idlisteimprimante = models.BigAutoField(primary_key=True)
    SN = models.CharField(verbose_name =_('Numeoro Série'),unique=True,max_length=50)
    reference = models.CharField(verbose_name =_('Référence'),max_length=50,null=False, blank=False,db_index=True)
    designation = models.CharField(verbose_name =_('Désignation'),max_length=50,null=False, blank=False,db_index=True)
    description = models.CharField(verbose_name =_('Description'),max_length=50,blank=True, null=True)
    date_acquisition = models.DateField(verbose_name =_('Date Acquisition'), blank=True, null=True)
    garantie = models.CharField(max_length=10,verbose_name =_('Garantie'), blank=True, null=True)
    endoflife = models.DateField(verbose_name =_('End of Life'), blank=True, null=True)
    flag = models.BooleanField(default=False)
    userLog = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)


    class Meta:
        managed = True
        db_table = 'leasing_listeimprimante'
        verbose_name = 'listeimprimante'
        verbose_name_plural = 'listeimprimantes'
        ordering = ["reference"]
    
    def __str__(self) -> str:
      return "{} {}".format(self.idlisteimprimante,self.designation)

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
    userLog = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
 
    class Meta:
        managed = True
        db_table = 'leasing_deploiement'
        verbose_name = 'deploiement'
        verbose_name_plural = 'deploiements'
        ordering = ["iddeploiement"]
    
    def __str__(self):
        return "{} - {} - {} - {}".format(self.site,self.clientleasing,self.listeimprimante,self.adresseip)
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
    class TypeConsommable(models.TextChoices):
        cartouche ="Cartouche", "Cartouche"
        photoconducteur = "Photoconducteur", "Photoconducteur"
        kits = "Kits", "Kits "
        fuser = "fuser LexMark", "Fuser LexMark"
        papier = "Papier RAM", "Papier RAM"
    class OrigineConsommable(models.TextChoices):
        hp ="HP","Produit HP"
        lexmark = "Produit LexMask","Produit LexMask"
        canon = "Produit Canon", "Produit Canon"
        AUTRE = "Autres", "Autres"
    idconsommable = models.BigAutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    bordereausortie = models.CharField(verbose_name =_('Bordereau SOP'), max_length=30,null=False, blank=False)
    categorieproduit = models.ForeignKey(typeCategorie,verbose_name =_('Catégorie'), on_delete=models.SET_DEFAULT,null=True,blank=True,default=None)
    typeproduit = models.CharField(verbose_name =_('Produit'),unique=False, max_length=30,null=False, blank=False)
    #categorieproduit = models.CharField(verbose_name =_('Catégorie'),max_length=30,
    #              choices=OrigineConsommable.choices,default=OrigineConsommable.lexmark)
    #typeproduit = models.CharField(max_length=20,verbose_name =_('Produit'),
    #                choices=TypeConsommable.choices,default = TypeConsommable.papier)
    reference = models.CharField(verbose_name =_('Référence'),unique=True, max_length=30,null=False, blank=False,db_index=True)
    designation = models.CharField(verbose_name =_('Désignation'),max_length=50,null=False, blank=False)
    description = models.CharField(verbose_name =_('Description'),max_length=100,null=True, blank=True)
    modele = models.CharField(verbose_name =_('Modele'), max_length=30,null=False, blank=False,db_index=True)
    
    quantite = models.IntegerField(verbose_name =_('Quantité'),default=0,null=False, blank=False)
    seuilLimite = models.IntegerField(verbose_name =_('Seuil'),default=5,null=False, blank=False)
    userLog = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    
    class Meta: 
        managed = True
        db_table = 'leasing_consommable'
        verbose_name = 'Consommable'
        verbose_name_plural = 'Consommables'
        ordering = ["-date","categorieproduit","typeproduit","reference"]
    
    def __str__(self) -> str:
       return "{}".format(self.reference,self.quantite)
       #return "{} - {} - {}".format(self.type,self.reference,self.quantite)

    @classmethod
    def select_conso_stock(cls):
        queryset = Consommable.objects.values('categorieproduit','typeproduit','reference','seuilLimite').annotate(stock=Sum('quantite')).order_by('categorieproduit','typeproduit','reference')
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
    idexploitation = models.BigAutoField(primary_key=True)
    date_exploitation = models.DateField(auto_now=True)
    intervention = models.CharField(max_length=50, verbose_name=_('Intervention'), choices=Typeintervention.choices, default=Typeintervention.papier)
    consommables = models.ManyToManyField(Consommable, through=ConsommableExploitation)
    deploiement = models.ForeignKey(Deploiement, on_delete=models.SET_NULL, null=True)
    pourcentage_toner = models.CharField(max_length=5, verbose_name=_('Toner (%)'), blank=True, null=True)
    ancien_index = models.IntegerField(blank=True, null=True)
    nouvel_index = models.IntegerField(blank=True, null=True)
    observation = models.TextField(verbose_name =_('Observation'),max_length=200,null=False, blank=False)
    

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
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
"""