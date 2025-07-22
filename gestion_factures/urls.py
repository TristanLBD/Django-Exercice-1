"""
URL configuration for gestion_factures project.

Configuration des URLs principales du projet de gestion de factures.
Ce fichier définit les routes de niveau projet et inclut les URLs de l'application facture.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from facture.views import index

# Configuration des URLs principales du projet
urlpatterns = [
    # Page d'accueil - affiche un aperçu des factures récentes
    path("", index, name="index"),

    # Interface d'administration Django
    path('admin/', admin.site.urls),

    # URLs de l'application facture (clients, catégories, factures)
    # Toutes les URLs commençant par '/' sont gérées par facture.urls
    path('', include('facture.urls')),
]
