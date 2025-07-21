from django.urls import path
from . import views

urlpatterns = [
    # URLs pour les clients
    path('clients/', views.ListeClientsView.as_view(), name='liste_clients'),
    path('clients/creer/', views.CreerClientView.as_view(), name='creer_client'),
    path('clients/<int:pk>/', views.DetailClientView.as_view(), name='detail_client'),
    path('clients/<int:pk>/modifier/', views.ModifierClientView.as_view(), name='modifier_client'),
    path('clients/<int:pk>/supprimer/', views.SupprimerClientView.as_view(), name='supprimer_client'),

    # URLs pour les factures
    path('factures/', views.ListeFacturesView.as_view(), name='liste_factures'),
    path('factures/creer/', views.CreerFactureView.as_view(), name='creer_facture'),
    path('factures/<int:pk>/', views.DetailFactureView.as_view(), name='detail_facture'),
    path('factures/<int:pk>/modifier/', views.ModifierFactureView.as_view(), name='modifier_facture'),
    path('factures/<int:pk>/supprimer/', views.SupprimerFactureView.as_view(), name='supprimer_facture'),

    # URLs pour les catégories
    path('categories/', views.ListeCategoriesView.as_view(), name='liste_categories'),
    path('categories/creer/', views.CreerCategorieView.as_view(), name='creer_categorie'),
    path('categories/<int:pk>/', views.DetailCategorieView.as_view(), name='detail_categorie'),
    path('categories/<int:pk>/modifier/', views.ModifierCategorieView.as_view(), name='modifier_categorie'),
    path('categories/<int:pk>/supprimer/', views.SupprimerCategorieView.as_view(), name='supprimer_categorie'),
]
