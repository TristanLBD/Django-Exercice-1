from django.contrib import admin
from .models import Categorie, Facture, Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'telephone', 'date_creation']
    search_fields = ['nom', 'email']
    list_filter = ['date_creation']
    ordering = ['nom']

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'couleur']
    search_fields = ['nom']
    list_filter = ['couleur']

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'date', 'montant', 'client', 'categorie', 'paye']
    list_filter = ['date', 'categorie', 'paye', 'client']
    search_fields = ['numero', 'client__nom']
    date_hierarchy = 'date'
    list_editable = ['paye']
