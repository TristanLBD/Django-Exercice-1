from django.db import models

# Create your models here.
class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    couleur = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

class Facture(models.Model):
    numero = models.CharField(max_length=255)
    date = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    paye = models.BooleanField(default=False, verbose_name="Payée")

    def __str__(self):
        return self.numero
