#!/usr/bin/env python
"""
Script de gestion Django pour l'application de gestion de factures.

Ce fichier est le point d'entrée principal pour toutes les commandes Django.
Il configure l'environnement et exécute les commandes de gestion.

Utilisation :
    python manage.py runserver     # Démarrer le serveur de développement
    python manage.py migrate       # Appliquer les migrations
    python manage.py makemigrations # Créer de nouvelles migrations
    python manage.py test          # Exécuter les tests
    python manage.py createsuperuser # Créer un utilisateur administrateur
"""
import os
import sys


def main():
    """
    Fonction principale qui configure l'environnement Django et exécute les commandes.

    Configure le module de paramètres par défaut et gère les erreurs d'importation
    si Django n'est pas installé ou accessible.
    """
    # Définir le module de paramètres par défaut pour ce projet
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_factures.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Exécuter la commande Django avec les arguments passés
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
