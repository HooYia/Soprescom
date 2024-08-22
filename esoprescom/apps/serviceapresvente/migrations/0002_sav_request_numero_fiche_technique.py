# Generated by Django 5.0.6 on 2024-08-22 09:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("serviceapresvente", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sav_request",
            name="numero_fiche_technique",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=30,
                null=True,
                unique=True,
                verbose_name="N° de Fiche Technique",
            ),
        ),
    ]
