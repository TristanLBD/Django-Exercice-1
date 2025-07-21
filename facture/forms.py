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
        fields = ['numero', 'date', 'montant', 'client', 'categorie', 'paye']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'paye': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
