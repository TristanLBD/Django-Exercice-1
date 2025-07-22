from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
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
class ListeCategoriesView(ListView):
    model = Categorie
    template_name = 'categories/liste.html'
    context_object_name = 'categories'
    ordering = ['nom']

class CreerCategorieView(CreateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'categories/creer.html'
    success_url = reverse_lazy('liste_categories')

class ModifierCategorieView(UpdateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'categories/modifier.html'

    def get_success_url(self):
        return reverse_lazy('detail_categorie', kwargs={'pk': self.object.pk})

class SupprimerCategorieView(DeleteView):
    model = Categorie
    template_name = 'categories/supprimer.html'
    success_url = reverse_lazy('liste_categories')

class DetailCategorieView(DetailView):
    model = Categorie
    template_name = 'categories/detail.html'
    context_object_name = 'categorie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['factures'] = Facture.objects.filter(categorie=self.object).order_by('-date')
        return context

# Vues pour les Clients
class ListeClientsView(ListView):
    model = Client
    template_name = 'clients/liste.html'
    context_object_name = 'clients'
    ordering = ['nom']

class CreerClientView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/creer.html'
    success_url = reverse_lazy('liste_clients')

class ModifierClientView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/modifier.html'

    def get_success_url(self):
        return reverse_lazy('detail_client', kwargs={'pk': self.object.pk})

class SupprimerClientView(DeleteView):
    model = Client
    template_name = 'clients/supprimer.html'
    success_url = reverse_lazy('liste_clients')

class DetailClientView(DetailView):
    model = Client
    template_name = 'clients/detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['factures'] = Facture.objects.filter(client=self.object).order_by('-date')
        return context

# Vues pour les Factures
class ListeFacturesView(ListView):
    model = Facture
    template_name = 'factures/liste.html'
    context_object_name = 'factures'
    ordering = ['-date']

    # pour filtrer les factures par client
    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.GET.get('client')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset

    # pour passer la liste des clients au template liste.html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all().order_by('nom')
        context['client_selectionne'] = self.request.GET.get('client')
        return context

class CreerFactureView(CreateView):
    model = Facture
    form_class = FactureForm
    template_name = 'factures/creer.html'
    success_url = reverse_lazy('liste_factures')

    def form_valid(self, form):
        # Sauvegarder d'abord la facture
        facture = form.save(commit=False)

        # Si aucune catégorie n'est sélectionnée, assigner "Autres"
        if not facture.categorie:
            categorie_autres, created = Categorie.objects.get_or_create(
                nom="Autres",
                defaults={'couleur': '#6c757d'}  # Couleur grise par défaut
            )
            facture.categorie = categorie_autres

        facture.save()
        return super().form_valid(form)

class ModifierFactureView(UpdateView):
    model = Facture
    form_class = FactureForm
    template_name = 'factures/modifier.html'

    def form_valid(self, form):
        # Sauvegarder d'abord la facture
        facture = form.save(commit=False)

        # Si aucune catégorie n'est sélectionnée, assigner "Autres"
        if not facture.categorie:
            categorie_autres, created = Categorie.objects.get_or_create(
                nom="Autres",
                defaults={'couleur': '#6c757d'}  # Couleur grise par défaut
            )
            facture.categorie = categorie_autres

        facture.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_facture', kwargs={'pk': self.object.pk})

class SupprimerFactureView(DeleteView):
    model = Facture
    template_name = 'factures/supprimer.html'
    success_url = reverse_lazy('liste_factures')

class DetailFactureView(DetailView):
    model = Facture
    template_name = 'factures/detail.html'
    context_object_name = 'facture'
