from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Categorie, Facture, Client
from .forms import CategorieForm, FactureForm, ClientForm


def index(request):
    """
    Vue d'accueil affichant un aperçu des dernières factures,
    des catégories et des clients.
    Utilise les méthodes du Manager et QuerySet personnalisés.
    """
    factures = Facture.objects.all()
    dernieres_factures = factures.order_by('-date')[:5]

    total_factures = factures.count()
    factures_payees = factures.payees().count()
    montant_total = factures.montant_total()

    categories = Categorie.objects.all()
    clients = Client.objects.all().order_by('nom')

    context = {
        'factures': dernieres_factures,
        'categories': categories,
        'clients': clients,
        'total_factures': total_factures,
        'factures_payees': factures_payees,
        'montant_total': montant_total,
    }
    return render(request, 'index.html', context)


# ===== VUES POUR LES CATÉGORIES =====

class ListeCategoriesView(ListView):
    """Vue pour afficher la liste de toutes les catégories."""
    model = Categorie
    template_name = 'categories/liste.html'
    context_object_name = 'categories'
    ordering = ['nom']


class CreerCategorieView(CreateView):
    """Vue pour créer une nouvelle catégorie."""
    model = Categorie
    form_class = CategorieForm
    template_name = 'categories/creer.html'
    success_url = reverse_lazy('liste_categories')


class ModifierCategorieView(UpdateView):
    """Vue pour modifier une catégorie existante."""
    model = Categorie
    form_class = CategorieForm
    template_name = 'categories/modifier.html'

    def get_success_url(self):
        return reverse_lazy('detail_categorie', kwargs={'pk': self.object.pk})


class SupprimerCategorieView(DeleteView):
    """Vue pour supprimer une catégorie."""
    model = Categorie
    template_name = 'categories/supprimer.html'
    success_url = reverse_lazy('liste_categories')


class DetailCategorieView(DetailView):
    """Vue pour afficher les détails d'une catégorie avec ses factures."""
    model = Categorie
    template_name = 'categories/detail.html'
    context_object_name = 'categorie'

    def get_context_data(self, **kwargs):
        """Ajoute la liste des factures de cette catégorie au contexte."""
        context = super().get_context_data(**kwargs)
        context['factures'] = Facture.objects.filter(categorie=self.object).order_by('-date')
        return context


# ===== VUES POUR LES CLIENTS =====

class ListeClientsView(ListView):
    """Vue pour afficher la liste de tous les clients."""
    model = Client
    template_name = 'clients/liste.html'
    context_object_name = 'clients'
    ordering = ['nom']


class CreerClientView(CreateView):
    """Vue pour créer un nouveau client."""
    model = Client
    form_class = ClientForm
    template_name = 'clients/creer.html'
    success_url = reverse_lazy('liste_clients')


class ModifierClientView(UpdateView):
    """Vue pour modifier un client existant."""
    model = Client
    form_class = ClientForm
    template_name = 'clients/modifier.html'

    def get_success_url(self):
        return reverse_lazy('detail_client', kwargs={'pk': self.object.pk})


class SupprimerClientView(DeleteView):
    """Vue pour supprimer un client."""
    model = Client
    template_name = 'clients/supprimer.html'
    success_url = reverse_lazy('liste_clients')


class DetailClientView(DetailView):
    """Vue pour afficher les détails d'un client avec ses factures."""
    model = Client
    template_name = 'clients/detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        """Ajoute la liste des factures de ce client au contexte."""
        context = super().get_context_data(**kwargs)
        context['factures'] = Facture.objects.filter(client=self.object).order_by('-date')
        return context


# ===== VUES POUR LES FACTURES =====

class ListeFacturesView(ListView):
    """
    Vue pour afficher la liste des factures avec filtres par client et catégorie.
    Supporte les filtres combinés via les paramètres GET 'client' et 'categorie'.
    """
    model = Facture
    template_name = 'factures/liste.html'
    context_object_name = 'factures'
    ordering = ['-date']

    def get_queryset(self):
        """
        Applique les filtres par client et/ou catégorie selon les paramètres GET.
        Utilise les méthodes du QuerySet personnalisé.
        """
        queryset = super().get_queryset()
        client_id = self.request.GET.get('client')
        categorie_id = self.request.GET.get('categorie')

        if client_id:
            queryset = queryset.par_client(client_id)
        if categorie_id:
            queryset = queryset.par_categorie(categorie_id)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Ajoute les listes de clients et catégories au contexte pour les filtres,
        ainsi que les valeurs actuellement sélectionnées.
        """
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all().order_by('nom')
        context['categories'] = Categorie.objects.all().order_by('nom')
        context['client_selectionne'] = self.request.GET.get('client')
        context['categorie_selectionnee'] = self.request.GET.get('categorie')
        return context


class CreerFactureView(CreateView):
    """
    Vue pour créer une nouvelle facture.
    Utilise la méthode du Manager pour l'assignation automatique.
    """
    model = Facture
    form_class = FactureForm
    template_name = 'factures/creer.html'
    success_url = reverse_lazy('liste_factures')

    def form_valid(self, form):
        """
        Utilise la méthode du Manager pour créer la facture avec
        assignation automatique de la catégorie "Autres" si nécessaire.
        """
        # Sauvegarder d'abord la facture
        facture = form.save(commit=False)

        # Si aucune catégorie n'est sélectionnée, assigner "Autres"
        if not facture.categorie:
            categorie_autres, created = Categorie.objects.get_or_create(
                nom="Autres",
                defaults={'couleur': '#6c757d'}
            )
            facture.categorie = categorie_autres

        facture.save()
        return super().form_valid(form)


class ModifierFactureView(UpdateView):
    """
    Vue pour modifier une facture existante.
    Implémente la même logique d'assignation automatique que la création.
    """
    model = Facture
    form_class = FactureForm
    template_name = 'factures/modifier.html'

    def form_valid(self, form):
        """
        Utilise la méthode du Manager pour modifier la facture avec
        assignation automatique de la catégorie "Autres" si nécessaire.
        """
        # Mettre à jour les champs de la facture existante
        facture = self.get_object()
        facture.numero = form.cleaned_data['numero']
        facture.date = form.cleaned_data['date']
        facture.montant_ht = form.cleaned_data['montant_ht']
        facture.taux_tva = form.cleaned_data['taux_tva']
        facture.client = form.cleaned_data['client']
        facture.paye = form.cleaned_data['paye']

        # Gérer la catégorie avec la logique du Manager
        if form.cleaned_data.get('categorie'):
            facture.categorie = form.cleaned_data['categorie']
        else:
            # Utiliser la même logique que le Manager
            categorie, created = Categorie.objects.get_or_create(
                nom='Autres',
                defaults={'couleur': '#6c757d'}
            )
            facture.categorie = categorie

        facture.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_facture', kwargs={'pk': self.object.pk})


class SupprimerFactureView(DeleteView):
    """Vue pour supprimer une facture."""
    model = Facture
    template_name = 'factures/supprimer.html'
    success_url = reverse_lazy('liste_factures')


class DetailFactureView(DetailView):
    """Vue pour afficher les détails d'une facture."""
    model = Facture
    template_name = 'factures/detail.html'
    context_object_name = 'facture'


def test_middleware_view(request):
    """
    Vue de test pour vérifier le fonctionnement du middleware.
    Affiche les logs de création de factures récents.
    """
    from .models import LogCreationFacture

    # Récupérer les 10 derniers logs
    logs = LogCreationFacture.objects.select_related('facture', 'facture__client').order_by('-date_creation')[:10]

    context = {
        'logs': logs,
        'total_logs': LogCreationFacture.objects.count(),
    }

    return render(request, 'test_middleware.html', context)
