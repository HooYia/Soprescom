# Generated by Django 5.0.6 on 2024-10-05 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_actionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionlog',
            name='type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
