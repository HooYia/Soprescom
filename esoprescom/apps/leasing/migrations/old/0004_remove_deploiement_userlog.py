# Generated by Django 5.0.1 on 2024-09-04 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leasing', '0003_remove_listeimprimante_userlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deploiement',
            name='userLog',
        ),
    ]
