# Gestion des Factures - Application Django

## 📋 Description

Application web Django pour la gestion complète de factures, clients et catégories.
Permet de créer, modifier, supprimer et consulter des factures avec calcul automatique
de la TVA et du TTC.

## ✨ Fonctionnalités principales

### 🧾 Gestion des Factures

-   **Création et modification** de factures avec interface intuitive
-   **Calcul automatique** de la TVA et du TTC basé sur le montant HT
-   **Filtrage avancé** par client et/ou catégorie
-   **Statut de paiement** avec indicateurs visuels
-   **Assignation automatique** à la catégorie "Autres" si aucune catégorie n'est sélectionnée

### 👥 Gestion des Clients

-   **Fiche client complète** avec coordonnées et adresse
-   **Historique des factures** par client
-   **Interface d'administration** avec recherche et filtres

### 🏷️ Gestion des Catégories

-   **Catégories personnalisables** avec couleurs d'affichage
-   **Organisation** des factures par type de service/produit
-   **Interface colorée** pour une meilleure visibilité

### 🔧 Interface d'Administration

-   **Actions en lot** pour marquer plusieurs factures comme payées
-   **Recherche avancée** par numéro de facture et client
-   **Filtres multiples** pour une gestion efficace
-   **Affichage coloré** du statut de paiement

## 🚀 Installation et Configuration

### Prérequis

-   Python 3.8 ou supérieur
-   pip (gestionnaire de paquets Python)

### Installation

1. **Cloner le projet**

```bash
git clone https://github.com/TristanLBD/Projet-Django.git
cd Projet-Django
```

2. **Créer un environnement virtuel**

```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Installer les dépendances**

```bash
pip install django
```

5. **Configurer la base de données**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Créer un utilisateur administrateur**

```bash
python manage.py createsuperuser
```

7. **Lancer le serveur de développement**

```bash
python manage.py runserver
```

8. **Accéder à l'application**

-   Interface utilisateur : http://127.0.0.1:8000/
-   Interface d'administration : http://127.0.0.1:8000/admin/

## 📁 Structure du Projet

```
Projet Django/
├── facture/                    # Application principale
│   ├── models.py              # Modèles de données (Client, Categorie, Facture)
│   ├── views.py               # Vues et logique métier
│   ├── forms.py               # Formulaires personnalisés
│   ├── admin.py               # Configuration de l'interface d'administration
│   ├── urls.py                # Configuration des URLs
│   ├── tests.py               # Tests unitaires et d'intégration
│   └── templates/             # Templates HTML
│       ├── index.html         # Page d'accueil
│       ├── clients/           # Templates pour la gestion des clients
│       ├── categories/        # Templates pour la gestion des catégories
│       └── factures/          # Templates pour la gestion des factures
├── gestion_factures/          # Configuration du projet
│   ├── settings.py            # Paramètres Django
│   ├── urls.py                # URLs principales
│   └── wsgi.py                # Configuration WSGI
├── manage.py                  # Script de gestion Django
└── README.md                  # Documentation du projet
```

## 🧪 Tests

L'application inclut une suite de tests complète :

### Tests des Modèles

-   Création et validation des factures
-   Calculs automatiques de TVA/TTC
-   Gestion des taux de TVA variables
-   Validation des montants négatifs

### Tests des Vues

-   Accès aux pages et formulaires
-   Filtrage des factures par client et catégorie
-   Création et modification de factures
-   Assignation automatique de catégories
-   Navigation et interface utilisateur

### Exécution des Tests

```bash
# Tous les tests
python manage.py test

# Tests spécifiques
python manage.py test facture.tests.FactureModelTest
python manage.py test facture.tests.FactureViewsTest
```

## 🔧 Configuration Avancée

### Variables d'Environnement

Pour la production, configurez les variables suivantes :

-   `SECRET_KEY` : Clé secrète Django
-   `DEBUG` : Mode debug (False en production)
-   `ALLOWED_HOSTS` : Hôtes autorisés
-   `DATABASE_URL` : URL de la base de données

### Base de Données

L'application utilise SQLite par défaut pour le développement.
Pour la production, configurez PostgreSQL ou MySQL dans `settings.py`.

## 📊 Fonctionnalités Métier

### Calculs Automatiques

-   **TVA** : `montant_tva = montant_ht × taux_tva / 100`
-   **TTC** : `montant_ttc = montant_ht + montant_tva`
-   **Taux par défaut** : 20% (configurable)

### Gestion des Catégories

-   **Catégorie "Autres"** : Créée automatiquement si nécessaire
-   **Couleurs personnalisées** : Interface visuelle améliorée
-   **Organisation** : Facilite le suivi par type de service

### Filtrage et Recherche

-   **Filtres combinés** : Client ET catégorie simultanément
-   **Recherche admin** : Par numéro de facture et nom de client
-   **Tri automatique** : Par date décroissante

## 🤝 Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🆘 Support

Pour toute question ou problème :

1. Consultez la documentation Django
2. Vérifiez les logs d'erreur
3. Exécutez les tests pour identifier les problèmes
4. Ouvrez une issue sur le repository

---

**Développé avec ❤️ en Django**
