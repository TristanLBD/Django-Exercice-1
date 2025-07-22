from django.db import models

# Create your models here.
class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    couleur = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

class Client(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom du client")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return self.nom

class Facture(models.Model):
    numero = models.CharField(max_length=255)
    date = models.DateField()
    montant_ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant HT")
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, verbose_name="Taux TVA (%)")
    montant_tva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant TVA", editable=False)
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant TTC", editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True)
    paye = models.BooleanField(default=False, verbose_name="Payée")

    def save(self, *args, **kwargs):
        # Calculer automatiquement la TVA et le TTC
        self.montant_tva = (self.montant_ht * self.taux_tva) / 100
        self.montant_ttc = self.montant_ht + self.montant_tva
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero
