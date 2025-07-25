# Generated by Django 5.1 on 2025-07-22 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0002_alter_facture_montant_ttc_alter_facture_montant_tva'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorie',
            options={'ordering': ['nom'], 'verbose_name': 'Catégorie', 'verbose_name_plural': 'Catégories'},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['nom'], 'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
        migrations.AlterModelOptions(
            name='facture',
            options={'ordering': ['-date', '-id'], 'verbose_name': 'Facture', 'verbose_name_plural': 'Factures'},
        ),
        migrations.AlterField(
            model_name='categorie',
            name='couleur',
            field=models.CharField(help_text='Code couleur hexadécimal (ex: #FF5733)', max_length=7, verbose_name="Couleur d'affichage"),
        ),
        migrations.AlterField(
            model_name='categorie',
            name='nom',
            field=models.CharField(max_length=255, verbose_name='Nom de la catégorie'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='categorie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='facture.categorie', verbose_name='Catégorie'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='date',
            field=models.DateField(verbose_name='Date de facturation'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='numero',
            field=models.CharField(max_length=255, verbose_name='Numéro de facture'),
        ),
        migrations.CreateModel(
            name='LogCreationFacture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création du log')),
                ('ip_utilisateur', models.GenericIPAddressField(verbose_name="Adresse IP de l'utilisateur")),
                ('user_agent', models.TextField(blank=True, null=True, verbose_name='User Agent')),
                ('methode_creation', models.CharField(help_text='Ex: formulaire web, API, import, etc.', max_length=50, verbose_name='Méthode de création')),
                ('details_supplementaires', models.JSONField(blank=True, help_text='Informations complémentaires en JSON', null=True, verbose_name='Détails supplémentaires')),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facture.facture', verbose_name='Facture créée')),
            ],
            options={
                'verbose_name': 'Log de création de facture',
                'verbose_name_plural': 'Logs de création de factures',
                'ordering': ['-date_creation'],
            },
        ),
    ]
