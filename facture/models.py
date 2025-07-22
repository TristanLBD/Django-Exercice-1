from django.db import models

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
