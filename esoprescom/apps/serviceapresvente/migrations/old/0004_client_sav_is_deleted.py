# Generated by Django 5.0.6 on 2024-08-27 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapresvente', '0003_client_sav_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='client_sav',
            name='is_deleted',
            field=models.BooleanField(default=True),
        ),
    ]
