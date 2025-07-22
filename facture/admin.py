from django.contrib import admin
from django.utils.html import format_html
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
    list_display = ['numero', 'date', 'montant_ht', 'montant_ttc', 'client', 'categorie', 'paye', 'statut_paye_colore']
    list_filter = ['date', 'categorie', 'paye', 'client']
    search_fields = ['numero', 'client__nom', 'client__email']
    date_hierarchy = 'date'
    list_editable = ['paye']
    actions = ['marquer_comme_paye', 'marquer_comme_non_paye']
    list_per_page = 25

    def statut_paye_colore(self, obj):
        """Affiche le statut de paiement avec des couleurs"""
        if obj.paye:
            return format_html('<span style="color: green; font-weight: bold;">✓ Payée</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">✗ Non payée</span>')
    statut_paye_colore.short_description = 'Statut'

    def marquer_comme_paye(self, request, queryset):
        """Action pour marquer les factures sélectionnées comme payées"""
        updated = queryset.update(paye=True)
        if updated == 1:
            message = "1 facture a été marquée comme payée."
        else:
            message = f"{updated} factures ont été marquées comme payées."
        self.message_user(request, message)
    marquer_comme_paye.short_description = "Marquer les factures sélectionnées comme payées"

    def marquer_comme_non_paye(self, request, queryset):
        """Action pour marquer les factures sélectionnées comme non payées"""
        updated = queryset.update(paye=False)
        if updated == 1:
            message = "1 facture a été marquée comme non payée."
        else:
            message = f"{updated} factures ont été marquées comme non payées."
        self.message_user(request, message)
    marquer_comme_non_paye.short_description = "Marquer les factures sélectionnées comme non payées"
