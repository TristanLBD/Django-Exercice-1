from django import forms
from .models import Categorie, Facture

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'couleur']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'couleur': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['numero', 'date', 'montant', 'categorie', 'paye']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'paye': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
