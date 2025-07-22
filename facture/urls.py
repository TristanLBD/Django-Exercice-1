"""
Configuration des URLs de l'application facture.

Ce fichier définit toutes les routes pour la gestion des clients,
catégories et factures. Chaque route suit le pattern RESTful standard
avec les opérations CRUD (Create, Read, Update, Delete).
"""
from django.urls import path
from . import views

# Configuration des URLs de l'application facture
urlpatterns = [
    # ===== GESTION DES CLIENTS =====
    # Routes pour la gestion complète des clients (CRUD)
    path('clients/', views.ListeClientsView.as_view(), name='liste_clients'),                    # Liste tous les clients
    path('clients/creer/', views.CreerClientView.as_view(), name='creer_client'),                # Formulaire de création
    path('clients/<int:pk>/', views.DetailClientView.as_view(), name='detail_client'),           # Détails d'un client
    path('clients/<int:pk>/modifier/', views.ModifierClientView.as_view(), name='modifier_client'), # Formulaire de modification
    path('clients/<int:pk>/supprimer/', views.SupprimerClientView.as_view(), name='supprimer_client'), # Confirmation de suppression

    # ===== GESTION DES FACTURES =====
    # Routes pour la gestion complète des factures (CRUD)
    # Supporte les filtres par client et catégorie via paramètres GET
    path('factures/', views.ListeFacturesView.as_view(), name='liste_factures'),                 # Liste toutes les factures
    path('factures/creer/', views.CreerFactureView.as_view(), name='creer_facture'),             # Formulaire de création
    path('factures/<int:pk>/', views.DetailFactureView.as_view(), name='detail_facture'),        # Détails d'une facture
    path('factures/<int:pk>/modifier/', views.ModifierFactureView.as_view(), name='modifier_facture'), # Formulaire de modification
    path('factures/<int:pk>/supprimer/', views.SupprimerFactureView.as_view(), name='supprimer_facture'), # Confirmation de suppression

    # ===== GESTION DES CATÉGORIES =====
    # Routes pour la gestion complète des catégories (CRUD)
    path('categories/', views.ListeCategoriesView.as_view(), name='liste_categories'),           # Liste toutes les catégories
    path('categories/creer/', views.CreerCategorieView.as_view(), name='creer_categorie'),       # Formulaire de création
    path('categories/<int:pk>/', views.DetailCategorieView.as_view(), name='detail_categorie'),  # Détails d'une catégorie
    path('categories/<int:pk>/modifier/', views.ModifierCategorieView.as_view(), name='modifier_categorie'), # Formulaire de modification
    path('categories/<int:pk>/supprimer/', views.SupprimerCategorieView.as_view(), name='supprimer_categorie'), # Confirmation de suppression
]
