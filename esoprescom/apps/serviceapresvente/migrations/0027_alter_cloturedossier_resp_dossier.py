# Generated by Django 5.0.6 on 2024-06-24 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapresvente', '0026_rename_numero_dossier_cloturedossier_numero_dossier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloturedossier',
            name='resp_dossier',
            field=models.CharField(default='None', max_length=30, verbose_name='Resp dossier'),
        ),
    ]
