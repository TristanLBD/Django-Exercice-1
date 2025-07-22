from django.db import models
from django.utils import timezone
from django.db.models import Q, Sum, Count
from decimal import Decimal


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

    def par_periode(self, date_debut, date_fin):
        """Retourne les factures dans une période donnée."""
        return self.filter(date__range=[date_debut, date_fin])

    def montant_total(self):
        """Calcule le montant total TTC de toutes les factures."""
        return self.aggregate(total=Sum('montant_ttc'))['total'] or Decimal('0.00')

    def montant_ht_total(self):
        """Calcule le montant total HT de toutes les factures."""
        return self.aggregate(total=Sum('montant_ht'))['total'] or Decimal('0.00')

    def montant_tva_total(self):
        """Calcule le montant total de TVA de toutes les factures."""
        return self.aggregate(total=Sum('montant_tva'))['total'] or Decimal('0.00')

    def statistiques_par_categorie(self):
        """Retourne les statistiques groupées par catégorie."""
        return self.values('categorie__nom').annotate(
            nombre=Count('id'),
            total_ht=Sum('montant_ht'),
            total_ttc=Sum('montant_ttc')
        ).order_by('-total_ttc')

    def statistiques_par_client(self):
        """Retourne les statistiques groupées par client."""
        return self.values('client__nom').annotate(
            nombre=Count('id'),
            total_ht=Sum('montant_ht'),
            total_ttc=Sum('montant_ttc')
        ).order_by('-total_ttc')

    def recherche_avancee(self, terme):
        """Recherche avancée dans les numéros et noms de clients."""
        return self.filter(
            Q(numero__icontains=terme) |
            Q(client__nom__icontains=terme) |
            Q(client__email__icontains=terme)
        )


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

    def creer_avec_categorie_autres(self, **kwargs):
        """
        Crée une facture en assignant automatiquement la catégorie 'Autres'
        si aucune catégorie n'est spécifiée.
        """
        if 'categorie' not in kwargs or kwargs['categorie'] is None:
            # Récupérer ou créer la catégorie 'Autres'
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


class Categorie(models.Model):
    """
    Modèle représentant une catégorie de facture.
    Permet d'organiser les factures par type de service ou produit.
    """
    nom = models.CharField(max_length=255, verbose_name="Nom de la catégorie")
    couleur = models.CharField(max_length=7, verbose_name="Couleur d'affichage",
                              help_text="Code couleur hexadécimal (ex: #FF5733)")

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']


class Client(models.Model):
    """
    Modèle représentant un client.
    Stocke les informations de contact et de facturation.
    """
    nom = models.CharField(max_length=255, verbose_name="Nom du client")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['nom']


class Facture(models.Model):
    """
    Modèle principal représentant une facture.
    Gère automatiquement les calculs de TVA et TTC.
    """
    numero = models.CharField(max_length=255, verbose_name="Numéro de facture")
    date = models.DateField(verbose_name="Date de facturation")
    montant_ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant HT")
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=20.00,
                                  verbose_name="Taux TVA (%)")
    montant_tva = models.DecimalField(max_digits=10, decimal_places=2,
                                     verbose_name="Montant TVA", editable=False)
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=2,
                                     verbose_name="Montant TTC", editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE,
                                 null=True, blank=True, verbose_name="Catégorie")
    paye = models.BooleanField(default=False, verbose_name="Payée")

    # Manager personnalisé
    objects = FactureManager()

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour calculer automatiquement
        la TVA et le TTC avant la sauvegarde.
        """
        # Calculer automatiquement la TVA et le TTC
        self.montant_tva = (self.montant_ht * self.taux_tva) / 100
        self.montant_ttc = self.montant_ht + self.montant_tva
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero} - {self.client.nom}"

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ['-date', '-id']


class LogCreationFacture(models.Model):
    """
    Modèle pour enregistrer les logs de création de factures.
    Utilisé par le middleware pour tracer toutes les créations de factures.
    """
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, verbose_name="Facture créée")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création du log")
    ip_utilisateur = models.GenericIPAddressField(verbose_name="Adresse IP de l'utilisateur")
    user_agent = models.TextField(blank=True, null=True, verbose_name="User Agent")
    methode_creation = models.CharField(max_length=50, verbose_name="Méthode de création",
                                       help_text="Ex: formulaire web, API, import, etc.")
    details_supplementaires = models.JSONField(blank=True, null=True,
                                              verbose_name="Détails supplémentaires",
                                              help_text="Informations complémentaires en JSON")

    def __str__(self):
        return f"Log création {self.facture.numero} - {self.date_creation}"

    class Meta:
        verbose_name = "Log de création de facture"
        verbose_name_plural = "Logs de création de factures"
        ordering = ['-date_creation']
