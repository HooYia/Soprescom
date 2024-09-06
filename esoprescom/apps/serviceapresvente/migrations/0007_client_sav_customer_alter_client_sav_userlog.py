# Generated by Django 5.0.6 on 2024-08-29 09:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapresvente', '0006_alter_client_sav_userlog'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='client_sav',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='client_sav',
            name='userLog',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='User Log'),
        ),
    ]
