from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Categorie, Facture, Client
from .forms import CategorieForm, FactureForm, ClientForm

# Vue d'accueil
def index(request):
    factures = Facture.objects.all().order_by('-date')[:5]
    categories = Categorie.objects.all()
    clients = Client.objects.all().order_by('nom')
    context = {
        'factures': factures,
        'categories': categories,
        'clients': clients,
    }
    return render(request, 'index.html', context)

# Vues pour les Catégories
def liste_categories(request):
    categories = Categorie.objects.all().order_by('nom')
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
            return redirect('detail_categorie', pk=categorie.pk)
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
    factures = Facture.objects.filter(categorie=categorie).order_by('-date')
    return render(request, 'categories/detail.html', {'categorie': categorie, 'factures': factures})

# Vues pour les Clients
def liste_clients(request):
    clients = Client.objects.all().order_by('nom')
    return render(request, 'clients/liste.html', {'clients': clients})

def creer_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_clients')
    else:
        form = ClientForm()
    return render(request, 'clients/creer.html', {'form': form})

def modifier_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('detail_client', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/modifier.html', {'form': form, 'client': client})

def supprimer_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('liste_clients')
    return render(request, 'clients/supprimer.html', {'client': client})

def detail_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    factures = Facture.objects.filter(client=client).order_by('-date')
    return render(request, 'clients/detail.html', {'client': client, 'factures': factures})

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
            return redirect('detail_facture', pk=facture.pk)
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
