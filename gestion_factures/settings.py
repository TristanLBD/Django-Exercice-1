"""
Django settings for gestion_factures project.

Configuration pour l'application de gestion de factures.
Ce fichier contient tous les paramètres de configuration Django.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ===== CONFIGURATION DE SÉCURITÉ =====
# ATTENTION: Ces paramètres sont pour le développement uniquement
# Voir https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Cette clé secrète doit être changée en production et stockée de manière sécurisée
SECRET_KEY = 'django-insecure-)7ms8on5b##=(rf)*510-^z6ff^e3b$)5dg07$^j)q2b)h7*wm'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG=True affiche des informations sensibles en cas d'erreur
DEBUG = True

# Liste des hôtes autorisés à accéder à l'application
ALLOWED_HOSTS = []


# ===== CONFIGURATION DES APPLICATIONS =====

INSTALLED_APPS = [
    # Applications Django par défaut
    'django.contrib.admin',      # Interface d'administration
    'django.contrib.auth',       # Système d'authentification
    'django.contrib.contenttypes', # Framework de types de contenu
    'django.contrib.sessions',   # Framework de sessions
    'django.contrib.messages',   # Framework de messages
    'django.contrib.staticfiles', # Gestion des fichiers statiques

    # Applications locales
    'facture',                   # Application principale de gestion des factures
]

# ===== MIDDLEWARE =====
# Les middlewares sont exécutés dans l'ordre pour chaque requête

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',            # Sécurité (HTTPS, etc.)
    'django.contrib.sessions.middleware.SessionMiddleware',     # Gestion des sessions
    'django.middleware.common.CommonMiddleware',                # Middleware commun
    'django.middleware.csrf.CsrfViewMiddleware',                # Protection CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentification
    'django.contrib.messages.middleware.MessageMiddleware',     # Messages flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Protection clickjacking
    'facture.middleware.LogCreationFactureMiddleware',          # Log des créations de factures
]

# Configuration des URLs racines
ROOT_URLCONF = 'gestion_factures.urls'

# ===== CONFIGURATION DES TEMPLATES =====

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Répertoires supplémentaires pour les templates
        'APP_DIRS': True,  # Chercher les templates dans les dossiers 'templates' des apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',      # Variables de debug
                'django.template.context_processors.request',    # Objet request
                'django.contrib.auth.context_processors.auth',   # Utilisateur connecté
                'django.contrib.messages.context_processors.messages', # Messages
            ],
        },
    },
]

# Configuration WSGI pour le déploiement
WSGI_APPLICATION = 'gestion_factures.wsgi.application'


# ===== CONFIGURATION DE LA BASE DE DONNÉES =====
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Base de données SQLite (développement)
        'NAME': BASE_DIR / 'db.sqlite3',         # Fichier de base de données
    }
}


# ===== VALIDATION DES MOTS DE PASSE =====
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # Empêche l'utilisation de mots de passe trop similaires aux informations utilisateur
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # Exige une longueur minimale pour les mots de passe
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # Empêche l'utilisation de mots de passe trop communs
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # Empêche l'utilisation de mots de passe entièrement numériques
    },
]


# ===== INTERNATIONALISATION =====
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr'          # Langue française
TIME_ZONE = 'Europe/Paris'       # Fuseau horaire français
USE_I18N = True                  # Activer l'internationalisation
USE_TZ = True                    # Activer la gestion des fuseaux horaires


# ===== FICHIERS STATIQUES =====
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'           # URL pour servir les fichiers statiques

# ===== CONFIGURATION PAR DÉFAUT =====

# Type de clé primaire par défaut pour les modèles
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
