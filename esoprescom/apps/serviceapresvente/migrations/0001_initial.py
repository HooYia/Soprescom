# Generated by Django 5.0.6 on 2024-09-27 17:23

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssemblageReparation',
            fields=[
                ('idassemblage', models.BigAutoField(primary_key=True, serialize=False)),
                ('statut', models.CharField(choices=[('pending (DSI - Assemblage)', 'pending (DSI - Assemblage)'), ('Terminé', 'Terminé')], default='pending (DSI - Assemblage)', max_length=30, verbose_name='Statut')),
                ('commentaire', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=200)])),
                ('flag', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fournisseurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-Mail')),
                ('adresse', models.CharField(max_length=200)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client_sav',
            fields=[
                ('idclient', models.BigAutoField(primary_key=True, serialize=False)),
                ('est_personne_morale', models.BooleanField(default=False)),
                ('raison_sociale', models.CharField(blank=True, max_length=255, null=True)),
                ('nom', models.CharField(blank=True, max_length=50, null=True)),
                ('prenom', models.CharField(blank=True, max_length=100, null=True)),
                ('telephone', models.CharField(max_length=50)),
                ('adresse', models.CharField(max_length=50)),
                ('client_name', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('userLog', models.CharField(blank=True, max_length=50, null=True, verbose_name='User Log')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('idinstance', models.BigAutoField(primary_key=True, serialize=False)),
                ('type_instance', models.CharField(choices=[('Interne', 'Interne'), ('Externe', 'Externe')], default='Externe', max_length=20, verbose_name='Instance')),
                ('numero_dossier', models.CharField(max_length=30, verbose_name='N° de Dossier')),
                ('besoin', models.CharField(blank=True, max_length=30, null=True, verbose_name='Besoin')),
                ('action', models.TextField(validators=[django.core.validators.MaxLengthValidator(limit_value=100)], verbose_name='Action')),
                ('statut', models.CharField(choices=[('En cour', 'En cour'), ('Recouvrement', 'Recouvrement'), ('Décision DG', 'Décision DG'), ('Clôturé', 'Clôturé'), ('Non résolu', 'Non résolu')], default='En cour', max_length=20, verbose_name='Statut')),
                ('is_facturable', models.BooleanField(default=False)),
                ('rapport_technique', models.ImageField(blank=True, null=True, upload_to='instance/%Y/%m/%d/')),
                ('flag', models.BooleanField(default=False)),
                ('flag2', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='serviceapresvente.client_sav')),
                ('userLog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Instance_recouvrement',
            fields=[
                ('idrecouv', models.BigAutoField(primary_key=True, serialize=False)),
                ('facture_reference', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='N° facture')),
                ('facture_montant', models.FloatField(default=0, verbose_name='Montant')),
                ('facture_statut', models.CharField(choices=[('Payé', 'Payé'), ('Non Payé', 'Non Payé')], default='Non Payé', max_length=20, verbose_name='Paiement')),
                ('flag', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='serviceapresvente.instance')),
            ],
        ),
        migrations.CreateModel(
            name='LivraisonClient',
            fields=[
                ('idlivraisonclient', models.BigAutoField(primary_key=True, serialize=False)),
                ('statut', models.CharField(choices=[('Sav livré', 'Sav livré'), ('Sav non livré', 'Sav non livré')], default='Sav non livré', max_length=30, verbose_name='Statut')),
                ('commentaire', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=50)])),
                ('flag', models.BooleanField(default=False)),
                ('bordereau_livraison', models.ImageField(blank=True, null=True, upload_to='sav/bordereau_livraison/%Y/%m/%d/')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assamblagereparation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assamblagereparations', to='serviceapresvente.assemblagereparation')),
            ],
        ),
        migrations.CreateModel(
            name='Partenaires',
            fields=[
                ('idpartenaire', models.BigAutoField(primary_key=True, serialize=False)),
                ('marque', models.CharField(max_length=30, unique=True, verbose_name='Marque')),
                ('description', models.TextField(blank=True, max_length=200, null=True, verbose_name='Description')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Personnels',
            fields=[
                ('idpersonnel', models.BigAutoField(primary_key=True, serialize=False)),
                ('departement', models.CharField(blank=True, max_length=30, null=True, verbose_name='Département')),
                ('poste', models.CharField(blank=True, max_length=30, null=True, verbose_name='Poste')),
                ('telephone', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Telephone')),
                ('email', models.EmailField(blank=True, default='sav@soprescom.net', max_length=30, null=True, unique=True, verbose_name='Email')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='instance',
            name='responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='serviceapresvente.personnels'),
        ),
        migrations.CreateModel(
            name='Recouvrement',
            fields=[
                ('idrecouvrement', models.BigAutoField(primary_key=True, serialize=False)),
                ('is_devea_request', models.BooleanField(default=False)),
                ('statut', models.CharField(choices=[('Sav payé', 'Sav payé'), ('Sav non payé', 'Sav non payé')], default='Sav non payé', max_length=30, verbose_name='Statut')),
                ('montant_client', models.FloatField(default=0)),
                ('facture_client', models.ImageField(blank=True, null=True, upload_to='sav/factures/%Y/%m/%d/')),
                ('deveaOrder', models.CharField(default='0000', max_length=30, verbose_name='Order')),
                ('transitaire', models.CharField(choices=[('TANSIT1', 'TANSIT1'), ('TANSIT2', 'TANSIT2')], default='TANSIT1', max_length=40, verbose_name='Statut')),
                ('numero_awd', models.CharField(blank=True, max_length=30, null=True, verbose_name='Numero DHL AWD')),
                ('montant_prestation', models.FloatField(default=0, verbose_name='Montant transitaire')),
                ('remise_documentaire', models.FloatField(blank=True, default=0, null=True, verbose_name='Remise documentaire')),
                ('droit_douane', models.FloatField(blank=True, default=0, null=True, verbose_name='Droit douane')),
                ('transport', models.FloatField(blank=True, default=0, null=True, verbose_name='Transport')),
                ('statutDevea', models.CharField(choices=[('facturation HP, a completer', 'facturation HP, a completer'), ('Dossier HP complet', 'Dossier HP complet'), ('Dossier HP payé', 'Dossier HP payé'), ('Dossier HP non payé', 'Dossier HP non payé')], default='facturation HP, a completer', max_length=40, verbose_name='Statut')),
                ('facture_transitaire', models.ImageField(blank=True, null=True, upload_to='sav/facture_transitaire/%Y/%m/%d/')),
                ('autre_piece', models.ImageField(blank=True, null=True, upload_to='sav/autres_pieces/%Y/%m/%d/')),
                ('commentaire', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=50)])),
                ('flag', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('livraisonclient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='livraisonclients', to='serviceapresvente.livraisonclient')),
            ],
        ),
        migrations.CreateModel(
            name='ClotureDossier',
            fields=[
                ('idcloturedossier', models.BigAutoField(primary_key=True, serialize=False)),
                ('numero_dossier', models.CharField(max_length=30, verbose_name='Numero_Dossier')),
                ('client', models.CharField(default='None', max_length=30, verbose_name='Client')),
                ('resp_dossier', models.CharField(default='None', max_length=30, verbose_name='Resp dossier')),
                ('statut', models.CharField(max_length=30, verbose_name='Clôture Dossier')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recouvrement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recouvrements', to='serviceapresvente.recouvrement')),
            ],
        ),
        migrations.CreateModel(
            name='Sav_request',
            fields=[
                ('idrequest', models.BigAutoField(primary_key=True, serialize=False)),
                ('type_sav', models.CharField(choices=[('DEVEA', 'DEVEA'), ('Non DEVEA', 'Non DEVEA')], default='DEVEA', max_length=20, verbose_name='Type SAV')),
                ('numero_dossier', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='N° de Dossier')),
                ('numero_fiche_technique', models.CharField(blank=True, db_index=True, max_length=30, null=True, unique=True, verbose_name='N° de Fiche Technique')),
                ('numero_serie', models.CharField(blank=True, max_length=30, null=True, verbose_name='N° de Serie')),
                ('reference', models.CharField(blank=True, max_length=30, null=True, verbose_name='Reference')),
                ('designation', models.CharField(blank=True, max_length=50, null=True, verbose_name='Désignation')),
                ('garantie', models.CharField(choices=[('Sous garantie', 'Sous garantie'), ('hors garantie', 'hors garantie')], default='Sous garantie', max_length=20, verbose_name='Garantie')),
                ('description_piece', models.CharField(blank=True, max_length=100, null=True, verbose_name='Descr Pièce')),
                ('reference_piece', models.CharField(blank=True, max_length=30, null=True, verbose_name='Ref Pièce')),
                ('pop', models.CharField(blank=True, max_length=30, verbose_name='POP')),
                ('statut', models.CharField(default='Diagnostique interne', max_length=50, verbose_name='Statut')),
                ('observation', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=200)], verbose_name='Observation')),
                ('rapport_technique', models.ImageField(blank=True, null=True, upload_to='sav/rapport_techniques/%Y/%m/%d/')),
                ('facture_fournisseur', models.ImageField(blank=True, null=True, upload_to='sav/facture_fournissseurs/%Y/%m/%d/')),
                ('facture_proforma', models.ImageField(blank=True, null=True, upload_to='sav/facture_proformas/%Y/%m/%d/')),
                ('bon_pour_accord', models.BooleanField(default=False)),
                ('flag', models.BooleanField(default=False)),
                ('recouvrement_hp', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client_sav', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='serviceapresvente.client_sav')),
                ('marque', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='serviceapresvente.partenaires')),
                ('resp_sav', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='serviceapresvente.personnels')),
                ('userLog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Facturation',
            fields=[
                ('idfacturation', models.BigAutoField(primary_key=True, serialize=False)),
                ('reference_facture', models.CharField(blank=True, max_length=20, null=True)),
                ('montant', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('facture_proforma', models.ImageField(blank=True, null=True, upload_to='sav/factures/%Y/%m/%d/')),
                ('bon_pour_accord', models.BooleanField(blank=True, default=False, null=True, verbose_name='Bon Pour Accord')),
                ('est_paye', models.BooleanField(blank=True, default=False, null=True)),
                ('commentaire', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=200)])),
                ('flag', models.BooleanField(blank=True, default=False, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('savrequest', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='serviceapresvente.sav_request')),
            ],
        ),
        migrations.CreateModel(
            name='CommandeSav',
            fields=[
                ('idcommandesav', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre_jour', models.IntegerField(default=0)),
                ('statut', models.CharField(choices=[('commande placée', 'commande placée'), ('pending (achat)', 'pending (achat)')], default='pending (achat)', max_length=30, verbose_name='Statut')),
                ('flag', models.BooleanField(default=False)),
                ('commentaire', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=200)])),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fournisseurs', to='serviceapresvente.fournisseurs')),
                ('savrequest', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sav_requests', to='serviceapresvente.sav_request')),
            ],
        ),
        migrations.CreateModel(
            name='SuiviCommandeSav',
            fields=[
                ('idsuivicommandesav', models.BigAutoField(primary_key=True, serialize=False)),
                ('statut', models.CharField(choices=[('pending (logistique)', 'pending (logistique)'), ('Réception dépôt France ', 'Réception dépôt France'), ('Reception dépôt Dubaï ', 'Réception dépôt Dubaï'), ('Sous Douane Malienne', 'Sous Douane Malienne'), ('Reçu', 'Reçu')], default='pending (logistique)', max_length=30, verbose_name='Statut')),
                ('flag', models.BooleanField(default=False)),
                ('nombre_jour', models.IntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('commentaire', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=200)])),
                ('commandesav', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='commandesavs', to='serviceapresvente.commandesav')),
            ],
        ),
        migrations.AddField(
            model_name='assemblagereparation',
            name='suivicommandesav',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='suivicommandesavs', to='serviceapresvente.suivicommandesav'),
        ),
    ]
