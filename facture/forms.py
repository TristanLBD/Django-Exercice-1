from django import forms
from .models import Categorie, Facture, Client


class CategorieForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier des catégories.
    Inclut un sélecteur de couleur pour personnaliser l'affichage.
    """
    class Meta:
        model = Categorie
        fields = ['nom', 'couleur']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'couleur': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }


class ClientForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier des clients.
    Gère les informations de contact et d'adresse.
    """
    class Meta:
        model = Client
        fields = ['nom', 'email', 'telephone', 'adresse']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FactureForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier des factures.
    Inclut la gestion des montants HT/TVA/TTC et l'assignation de catégories.
    Les champs montant_tva et montant_ttc sont calculés automatiquement.
    """
    class Meta:
        model = Facture
        fields = ['numero', 'date', 'montant_ht', 'taux_tva', 'client', 'categorie', 'paye']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'montant_ht': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'taux_tva': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'paye': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialise le formulaire avec des labels et placeholders personnalisés.
        Configure l'option vide pour la catégorie avec un message explicatif.
        """
        super().__init__(*args, **kwargs)
        # Ajouter une option vide pour permettre de ne pas sélectionner de catégorie
        self.fields['categorie'].empty_label = "Aucune catégorie (sera assignée à 'Autres')"
        # Ajouter des labels plus clairs
        self.fields['montant_ht'].label = "Montant HT (€)"
        self.fields['taux_tva'].label = "Taux TVA (%)"
        # Ajouter des placeholders informatifs
        self.fields['montant_ht'].widget.attrs['placeholder'] = "Ex: 100.00"
        self.fields['taux_tva'].widget.attrs['placeholder'] = "Ex: 20.00"
