# Generated by Django 5.0.1 on 2024-09-03 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeasingClient',
            fields=[
                ('idclientleasing', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(db_index=True, max_length=25, unique=True, verbose_name='Nom')),
                ('adresse', models.CharField(max_length=100, verbose_name='Adresse')),
                ('contact', models.CharField(max_length=50, verbose_name='Contact')),
                ('localite', models.CharField(max_length=20, verbose_name='Région')),
                ('refcontrat', models.CharField(max_length=20, unique=True, verbose_name='N° Contrat ')),
                ('duree_contrat', models.CharField(max_length=10, verbose_name='Durée Contrat ')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='Email')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date Contrat')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='clientleasing',
            name='userLog',
        ),
        migrations.DeleteModel(
            name='HistioriqueConsommable',
        ),
        migrations.AlterField(
            model_name='consommable',
            name='categorieproduit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='leasing.listeimprimante', verbose_name='Catégorie'),
        ),
        migrations.AlterModelOptions(
            name='consommable',
            options={},
        ),
        migrations.AlterModelOptions(
            name='deploiement',
            options={},
        ),
        migrations.AlterModelOptions(
            name='listeimprimante',
            options={},
        ),
        migrations.RenameField(
            model_name='listeimprimante',
            old_name='SN',
            new_name='numero_serie',
        ),
        migrations.AlterModelTable(
            name='consommable',
            table=None,
        ),
        migrations.AlterModelTable(
            name='deploiement',
            table=None,
        ),
        migrations.AlterModelTable(
            name='listeimprimante',
            table=None,
        ),
        migrations.AlterField(
            model_name='deploiement',
            name='clientleasing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leasing.leasingclient'),
        ),
        migrations.DeleteModel(
            name='typeProduit',
        ),
        migrations.DeleteModel(
            name='typeCategorie',
        ),
        migrations.DeleteModel(
            name='Clientleasing',
        ),
    ]
