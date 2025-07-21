from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Categorie, Facture
from .forms import CategorieForm, FactureForm

# Vue d'accueil
def index(request):
    factures = Facture.objects.all().order_by('-date')
    categories = Categorie.objects.all()
    context = {
        'factures': factures,
        'categories': categories,
    }
    return render(request, 'index.html', context)

# Vues pour les Catégories
def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'categories/liste.html', {'categories': categories})

def creer_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_categories')
    else:
        form = CategorieForm()
    return render(request, 'categories/creer.html', {'form': form})

def modifier_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return redirect('liste_categories')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'categories/modifier.html', {'form': form, 'categorie': categorie})

def supprimer_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        categorie.delete()
        return redirect('liste_categories')
    return render(request, 'categories/supprimer.html', {'categorie': categorie})

def detail_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    factures = Facture.objects.filter(categorie=categorie)
    return render(request, 'categories/detail.html', {'categorie': categorie, 'factures': factures})

# Vues pour les Factures
def liste_factures(request):
    factures = Facture.objects.all().order_by('-date')
    return render(request, 'factures/liste.html', {'factures': factures})

def creer_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_factures')
    else:
        form = FactureForm()
    return render(request, 'factures/creer.html', {'form': form})

def modifier_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        form = FactureForm(request.POST, instance=facture)
        if form.is_valid():
            form.save()
            return redirect('liste_factures')
    else:
        form = FactureForm(instance=facture)
    return render(request, 'factures/modifier.html', {'form': form, 'facture': facture})

def supprimer_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        facture.delete()
        return redirect('liste_factures')
    return render(request, 'factures/supprimer.html', {'facture': facture})

def detail_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    return render(request, 'factures/detail.html', {'facture': facture})
