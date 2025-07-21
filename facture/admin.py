from django.contrib import admin
from .models import Categorie, Facture

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'couleur']
    search_fields = ['nom']
    list_filter = ['couleur']

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'date', 'montant', 'categorie', 'paye']
    list_filter = ['date', 'categorie', 'paye']
    search_fields = ['numero']
    date_hierarchy = 'date'
    list_editable = ['paye']
