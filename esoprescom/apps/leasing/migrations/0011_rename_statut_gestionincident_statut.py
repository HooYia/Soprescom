# Generated by Django 5.0.6 on 2024-09-09 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0010_remove_maintenance_id_gestionincident_teamsav_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gestionincident',
            old_name='Statut',
            new_name='statut',
        ),
    ]
