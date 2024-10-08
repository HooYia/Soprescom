# Generated by Django 5.0.1 on 2024-09-04 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0004_remove_deploiement_userlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('idcategorie', models.BigAutoField(primary_key=True, serialize=False)),
                ('categorie', models.CharField(choices=[('HP', 'Hp'), ('LEXMARK', 'LexMark'), ('CANON', 'CANON'), ('PAPIER', 'PAPIER')], max_length=15, verbose_name='Catégorie')),
                ('produit', models.CharField(choices=[('IMPRIMANTE', 'Imprimante'), ('CONSUMMABLE', 'Consommable')], max_length=15, verbose_name='Produit')),
                ('reference', models.CharField(max_length=30, verbose_name='Référence')),
                ('designation', models.CharField(max_length=30, verbose_name='Désignation')),
                ('descriptif', models.CharField(max_length=30, verbose_name='Descriptif')),
                ('image', models.ImageField(blank=True, null=True, upload_to='leasing/')),
            ],
        ),
        migrations.RemoveField(
            model_name='consommable',
            name='categorieproduit',
        ),
        migrations.RemoveField(
            model_name='typeproduit',
            name='categorie',
        ),
        migrations.AlterModelOptions(
            name='consommable',
            options={'managed': True, 'verbose_name': 'Consommable', 'verbose_name_plural': 'Consommables'},
        ),
        migrations.AlterModelOptions(
            name='listeimprimante',
            options={'managed': True, 'verbose_name': 'listeimprimante', 'verbose_name_plural': 'listeimprimantes'},
        ),
        migrations.RemoveField(
            model_name='consommable',
            name='description',
        ),
        migrations.RemoveField(
            model_name='consommable',
            name='designation',
        ),
        migrations.RemoveField(
            model_name='consommable',
            name='modele',
        ),
        migrations.RemoveField(
            model_name='consommable',
            name='reference',
        ),
        migrations.RemoveField(
            model_name='consommable',
            name='typeproduit',
        ),
        migrations.RemoveField(
            model_name='consommable',
            name='userLog',
        ),
        migrations.RemoveField(
            model_name='listeimprimante',
            name='description',
        ),
        migrations.RemoveField(
            model_name='listeimprimante',
            name='designation',
        ),
        migrations.RemoveField(
            model_name='listeimprimante',
            name='reference',
        ),
        migrations.AddField(
            model_name='listeimprimante',
            name='categorieproduit',
            field=models.ManyToManyField(to='leasing.categorie'),
        ),
        migrations.AddField(
            model_name='consommable',
            name='categorieproduit',
            field=models.ManyToManyField(to='leasing.categorie'),
        ),
        migrations.DeleteModel(
            name='typeCategorie',
        ),
        migrations.DeleteModel(
            name='typeProduit',
        ),
    ]
