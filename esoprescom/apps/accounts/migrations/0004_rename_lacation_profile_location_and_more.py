# Generated by Django 5.0.6 on 2024-10-02 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_lacation_profile_oraganisation_profile_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Lacation',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='Oraganisation',
            new_name='oraganisation',
        ),
    ]
