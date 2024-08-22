# Generated by Django 5.0.6 on 2024-06-13 15:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapresvente', '0019_remove_devea_autre_piece_remove_devea_commentaire_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cloturedossier',
            name='recouvrement',
        ),
        migrations.AddField(
            model_name='cloturedossier',
            name='Client',
            field=models.CharField(default='None', max_length=30, verbose_name='Client'),
        ),
        migrations.AddField(
            model_name='cloturedossier',
            name='Numero_Dossier',
            field=models.CharField(default='None', max_length=30, verbose_name='Numero_Dossier'),
        ),
        migrations.AddField(
            model_name='cloturedossier',
            name='recouvrement_ID',
            field=models.CharField(default='None', max_length=30, verbose_name='Recouvrement'),
        ),
        migrations.AddField(
            model_name='cloturedossier',
            name='recouvrement_Type',
            field=models.CharField(default='None', max_length=30, verbose_name='Recouvrement'),
        ),
        migrations.AddField(
            model_name='recouvrementdevea',
            name='transitaire',
            field=models.CharField(choices=[('TANSIT1', 'TANSIT1'), ('TANSIT2', 'TANSIT2')], default='TANSIT1', max_length=40, verbose_name='Statut'),
        ),
        migrations.AlterField(
            model_name='cloturedossier',
            name='commentaire',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=50)]),
        ),
    ]
