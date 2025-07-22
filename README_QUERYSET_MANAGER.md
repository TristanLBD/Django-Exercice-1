# QuerySets et Managers Django - Guide Complet

## 📚 Introduction

### Qu'est-ce qu'un QuerySet ?

Un **QuerySet** est une collection d'objets de base de données en Django. C'est comme une "requête SQL" mais écrite en Python. Il permet de :

-   **Filtrer** les données selon des critères
-   **Trier** les résultats
-   **Limiter** le nombre d'objets retournés
-   **Effectuer des opérations en lot** (calculs, agrégations)

### Qu'est-ce qu'un Manager ?

Un **Manager** est l'interface entre le modèle Django et la base de données. C'est lui qui :

-   **Gère les QuerySets** et fournit les méthodes de base (`all()`, `filter()`, `create()`)
-   **Permet d'ajouter des méthodes personnalisées** pour des opérations spécifiques
-   **Centralise la logique métier** liée à la création et récupération d'objets

---

## 🔍 QuerySets vs Managers : Différence

### **QuerySet** = Méthodes de **filtrage et analyse**

```python
# QuerySet : "Donne-moi les factures payées"
Facture.objects.filter(paye=True)

# QuerySet : "Calcule le total des factures"
Facture.objects.aggregate(total=Sum('montant_ttc'))
```

### **Manager** = Méthodes de **création et logique métier**

```python
# Manager : "Crée une facture avec catégorie automatique"
Facture.objects.creer_avec_categorie_autres(...)

# Manager : "Donne-moi les factures du mois"
Facture.objects.factures_du_mois()
```

---

## 🏗️ Architecture dans notre Projet

### **1. QuerySet Personnalisé (`FactureQuerySet`)**

```python
class FactureQuerySet(models.QuerySet):
    """
    QuerySet personnalisé pour le modèle Facture.
    Fournit des méthodes de filtrage et d'analyse avancées.
    """

    def payees(self):
        """Retourne toutes les factures payées."""
        return self.filter(paye=True)

    def non_payees(self):
        """Retourne toutes les factures non payées."""
        return self.filter(paye=False)

    def par_client(self, client_id):
        """Retourne toutes les factures d'un client spécifique."""
        return self.filter(client_id=client_id)

    def par_categorie(self, categorie_id):
        """Retourne toutes les factures d'une catégorie spécifique."""
        return self.filter(categorie_id=categorie_id)

    def montant_total(self):
        """Calcule le montant total TTC de toutes les factures."""
        return self.aggregate(total=Sum('montant_ttc'))['total'] or Decimal('0.00')

    def montant_ht_total(self):
        """Calcule le montant total HT de toutes les factures."""
        return self.aggregate(total=Sum('montant_ht'))['total'] or Decimal('0.00')

    def montant_tva_total(self):
        """Calcule le montant total de TVA de toutes les factures."""
        return self.aggregate(total=Sum('montant_tva'))['total'] or Decimal('0.00')

    def recherche_avancee(self, terme):
        """Recherche avancée dans les numéros et noms de clients."""
        return self.filter(
            Q(numero__icontains=terme) |
            Q(client__nom__icontains=terme) |
            Q(client__email__icontains=terme)
        )
```

### **2. Manager Personnalisé (`FactureManager`)**

```python
class FactureManager(models.Manager):
    """
    Manager personnalisé pour le modèle Facture.
    Fournit des méthodes de création et d'analyse avancées.
    """

    def get_queryset(self):
        """Retourne le QuerySet personnalisé."""
        return FactureQuerySet(self.model, using=self._db)

    # Méthodes du QuerySet accessibles via le Manager
    def payees(self):
        return self.get_queryset().payees()

    def non_payees(self):
        return self.get_queryset().non_payees()

    def par_client(self, client_id):
        return self.get_queryset().par_client(client_id)

    def par_categorie(self, categorie_id):
        return self.get_queryset().par_categorie(categorie_id)

    def montant_total(self):
        return self.get_queryset().montant_total()

    def montant_ht_total(self):
        return self.get_queryset().montant_ht_total()

    def montant_tva_total(self):
        return self.get_queryset().montant_tva_total()

    def recherche_avancee(self, terme):
        return self.get_queryset().recherche_avancee(terme)

    # Méthodes spécifiques au Manager
    def creer_avec_categorie_autres(self, **kwargs):
        """
        Crée une facture en assignant automatiquement la catégorie 'Autres'
        si aucune catégorie n'est spécifiée.
        """
        if 'categorie' not in kwargs or kwargs['categorie'] is None:
            categorie, created = Categorie.objects.get_or_create(
                nom='Autres',
                defaults={'couleur': '#6c757d'}
            )
            kwargs['categorie'] = categorie

        return self.create(**kwargs)

    def factures_du_mois(self):
        """Retourne toutes les factures du mois en cours."""
        aujourd_hui = timezone.now().date()
        debut_mois = aujourd_hui.replace(day=1)
        fin_mois = (debut_mois.replace(day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)

        return self.get_queryset().par_periode(debut_mois, fin_mois)

    def factures_de_l_annee(self, annee=None):
        """Retourne toutes les factures d'une année donnée."""
        if annee is None:
            annee = timezone.now().year

        debut_annee = timezone.datetime(annee, 1, 1).date()
        fin_annee = timezone.datetime(annee, 12, 31).date()

        return self.get_queryset().par_periode(debut_annee, fin_annee)

    def top_clients(self, limite=5):
        """Retourne les clients avec le plus de factures."""
        return self.get_queryset().statistiques_par_client()[:limite]

    def top_categories(self, limite=5):
        """Retourne les catégories avec le plus de factures."""
        return self.get_queryset().statistiques_par_categorie()[:limite]
```

### **3. Intégration dans le Modèle**

```python
class Facture(models.Model):
    numero = models.CharField(max_length=255, verbose_name="Numéro de facture")
    date = models.DateField(verbose_name="Date de facturation")
    montant_ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant HT")
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, verbose_name="Taux TVA (%)")
    montant_tva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant TVA", editable=False)
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant TTC", editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Catégorie")
    paye = models.BooleanField(default=False, verbose_name="Payée")

    # Manager personnalisé
    objects = FactureManager()
```

---

## 🚀 Utilisation Pratique

### **Avant (Code Complexe) :**

```python
# Dans les vues
def index(request):
    # Récupération complexe
    factures_payees = Facture.objects.filter(paye=True).count()
    montant_total = Facture.objects.aggregate(total=Sum('montant_ttc'))['total'] or Decimal('0.00')

    # Filtrage complexe
    factures_client = Facture.objects.filter(client_id=client_id)
    factures_categorie = Facture.objects.filter(categorie_id=categorie_id)

    # Recherche complexe
    factures_recherche = Facture.objects.filter(
        Q(numero__icontains=terme) |
        Q(client__nom__icontains=terme)
    )

# Dans les vues de création
def form_valid(self, form):
    facture = form.save(commit=False)
    if not facture.categorie:
        categorie, created = Categorie.objects.get_or_create(
            nom='Autres', defaults={'couleur': '#6c757d'}
        )
        facture.categorie = categorie
    facture.save()
```

### **Après (Code Simplifié) :**

```python
# Dans les vues
def index(request):
    factures = Facture.objects.all()

    # Utilisation des méthodes personnalisées
    factures_payees = factures.payees().count()
    montant_total = factures.montant_total()

    # Filtrage simplifié
    factures_client = factures.par_client(client_id)
    factures_categorie = factures.par_categorie(categorie_id)

    # Recherche simplifiée
    factures_recherche = factures.recherche_avancee(terme)

# Dans les vues de création
def form_valid(self, form):
    # Utilisation de la méthode du Manager
    facture = Facture.objects.creer_avec_categorie_autres(**form.cleaned_data)
```

---

## 📊 Exemples d'Utilisation

### **1. Méthodes QuerySet (Filtrage et Analyse)**

```python
# Récupérer toutes les factures payées
factures_payees = Facture.objects.payees()

# Récupérer toutes les factures non payées
factures_non_payees = Facture.objects.non_payees()

# Récupérer les factures d'un client spécifique
factures_client = Facture.objects.par_client(client_id=1)

# Récupérer les factures d'une catégorie spécifique
factures_categorie = Facture.objects.par_categorie(categorie_id=2)

# Calculer le montant total TTC
total_ttc = Facture.objects.montant_total()

# Calculer le montant total HT
total_ht = Facture.objects.montant_ht_total()

# Calculer le montant total de TVA
total_tva = Facture.objects.montant_tva_total()

# Recherche avancée
resultats = Facture.objects.recherche_avancee("FAC-2024")
```

### **2. Méthodes Manager (Création et Logique Métier)**

```python
# Créer une facture avec assignation automatique de catégorie
facture = Facture.objects.creer_avec_categorie_autres(
    numero="FAC-2024-001",
    date="2024-01-15",
    montant_ht=Decimal("100.00"),
    taux_tva=Decimal("20.00"),
    client=client,
    paye=False
)

# Récupérer les factures du mois en cours
factures_mois = Facture.objects.factures_du_mois()

# Récupérer les factures d'une année spécifique
factures_2024 = Facture.objects.factures_de_l_annee(2024)

# Récupérer les top 5 clients
top_clients = Facture.objects.top_clients(5)

# Récupérer les top 3 catégories
top_categories = Facture.objects.top_categories(3)
```

---

## 🎯 Avantages des QuerySets et Managers Personnalisés

### **1. Code Plus Lisible**

```python
# Avant
Facture.objects.filter(paye=True).aggregate(total=Sum('montant_ttc'))

# Après
Facture.objects.payees().montant_total()
```

### **2. Réutilisabilité**

-   **Une seule définition** de la logique
-   **Utilisation partout** dans le projet
-   **Modifications centralisées**

### **3. Maintenance Simplifiée**

-   **Logique métier centralisée**
-   **Tests spécifiques** pour chaque méthode
-   **Évolution facile** des fonctionnalités

### **4. Performance Optimisée**

-   **Requêtes optimisées** dans le QuerySet
-   **Cache automatique** des résultats
-   **Évite les requêtes N+1**

### **5. Expressivité**

-   **Noms explicites** des méthodes
-   **Intention claire** du code
-   **Documentation intégrée**

---

## 🧪 Tests

### **Tests QuerySet**

```python
class FactureQuerySetTest(TestCase):
    def test_payees(self):
        """Test de la méthode payees()."""
        factures_payees = Facture.objects.payees()
        self.assertEqual(factures_payees.count(), 2)

    def test_montant_total(self):
        """Test de la méthode montant_total()."""
        total = Facture.objects.montant_total()
        self.assertEqual(total, Decimal("525.00"))
```

### **Tests Manager**

```python
class FactureManagerTest(TestCase):
    def test_creer_avec_categorie_autres(self):
        """Test de la méthode creer_avec_categorie_autres()."""
        facture = Facture.objects.creer_avec_categorie_autres(
            numero="FAC-TEST-001",
            date="2024-01-01",
            montant_ht=Decimal("100.00"),
            taux_tva=Decimal("20.00"),
            client=self.client,
            paye=False
        )

        self.assertEqual(facture.categorie.nom, "Autres")
```

---

## 🔧 Bonnes Pratiques

### **1. Nommage des Méthodes**

-   **QuerySet** : Verbes d'action (`payees()`, `par_client()`)
-   **Manager** : Actions métier (`creer_avec_categorie_autres()`)

### **2. Documentation**

-   **Docstrings** explicites pour chaque méthode
-   **Exemples d'utilisation** dans les commentaires
-   **Types de retour** documentés

### **3. Tests Complets**

-   **Tests unitaires** pour chaque méthode
-   **Tests d'intégration** pour les cas complexes
-   **Tests de performance** pour les requêtes lourdes

### **4. Évolution**

-   **Méthodes extensibles** pour de futures fonctionnalités
-   **Compatibilité** avec les versions précédentes
-   **Migration** progressive des anciens usages

---

## 🎉 Conclusion

Les **QuerySets et Managers personnalisés** transforment le code Django en :

-   **Code plus expressif** et lisible
-   **Logique métier centralisée** et réutilisable
-   **Maintenance simplifiée** et évolutive
-   **Performance optimisée** et testable

Ils représentent une **évolution naturelle** de Django vers un code plus **maintenable** et **professionnel** ! 🚀
