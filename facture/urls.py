from django.urls import path
from . import views

urlpatterns = [
    # URLs pour les factures
    path('factures/', views.liste_factures, name='liste_factures'),
    path('factures/creer/', views.creer_facture, name='creer_facture'),
    path('factures/<int:pk>/', views.detail_facture, name='detail_facture'),
    path('factures/<int:pk>/modifier/', views.modifier_facture, name='modifier_facture'),
    path('factures/<int:pk>/supprimer/', views.supprimer_facture, name='supprimer_facture'),

    # URLs pour les catégories
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/creer/', views.creer_categorie, name='creer_categorie'),
    path('categories/<int:pk>/', views.detail_categorie, name='detail_categorie'),
    path('categories/<int:pk>/modifier/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/<int:pk>/supprimer/', views.supprimer_categorie, name='supprimer_categorie'),
]
