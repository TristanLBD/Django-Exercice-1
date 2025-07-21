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
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    paye = models.BooleanField(default=False, verbose_name="Payée")

    def __str__(self):
        return self.numero
