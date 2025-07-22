from django import forms
from .models import Categorie, Facture, Client

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'couleur']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'couleur': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }

class ClientForm(forms.ModelForm):
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
        super().__init__(*args, **kwargs)
        # Ajouter une option vide pour permettre de ne pas sélectionner de catégorie
        self.fields['categorie'].empty_label = "Aucune catégorie (sera assignée à 'Autres')"
        # Ajouter des labels plus clairs
        self.fields['montant_ht'].label = "Montant HT (€)"
        self.fields['taux_tva'].label = "Taux TVA (%)"
        # Ajouter des placeholders informatifs
        self.fields['montant_ht'].widget.attrs['placeholder'] = "Ex: 100.00"
        self.fields['taux_tva'].widget.attrs['placeholder'] = "Ex: 20.00"
