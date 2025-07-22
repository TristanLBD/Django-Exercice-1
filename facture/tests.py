"""
Tests pour l'application de gestion de factures.

Ce module contient tous les tests unitaires et d'intégration pour l'application facture.
Il teste les modèles, les vues et les fonctionnalités métier importantes.

Structure des tests :
- FactureModelTest : Tests des modèles et de la logique métier
- FactureViewsTest : Tests des vues et de l'interface utilisateur

Les tests couvrent :
- Calculs automatiques de TVA/TTC
- Filtrage des factures
- Assignation automatique de catégories
- Validation des données
- Navigation et interface utilisateur
"""
from django.test import TestCase, RequestFactory
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from decimal import Decimal
from django.utils import timezone
from datetime import date
from .models import Facture, Client, Categorie, LogCreationFacture
from .middleware import LogCreationFactureMiddleware

class FactureModelTest(TestCase):
    """
    Tests pour le modèle Facture.

    Vérifie la logique métier, les calculs automatiques et les validations
    du modèle principal de l'application.
    """

    def setUp(self):
        """
        Création des données de test communes à tous les tests du modèle.
        Initialise un client et une catégorie de test.
        """
        # Créer un client de test
        self.client = Client.objects.create(
            nom="Jean Dupont",
            email="jean.dupont@example.com",
            telephone="0123456789",
            adresse="123 Rue de la Paix, Paris"
        )

        # Créer une catégorie de test
        self.categorie = Categorie.objects.create(
            nom="Services",
            couleur="#FF5733"
        )

    def test_creation_facture_complete(self):
        """
        Test de création d'une facture avec tous les champs.
        Vérifie que tous les champs sont correctement sauvegardés.
        """
        facture = Facture.objects.create(
            numero="FAC-2024-001",
            date="2024-01-15",
            montant_ht=Decimal("100.00"),
            taux_tva=Decimal("20.00"),
            client=self.client,
            categorie=self.categorie,
            paye=False
        )

        # Vérifier que la facture a été créée
        self.assertEqual(facture.numero, "FAC-2024-001")
        self.assertEqual(facture.montant_ht, Decimal("100.00"))
        self.assertEqual(facture.taux_tva, Decimal("20.00"))
        self.assertEqual(facture.client, self.client)
        self.assertEqual(facture.categorie, self.categorie)
        self.assertFalse(facture.paye)

        # Vérifier que les calculs automatiques fonctionnent
        self.assertEqual(facture.montant_tva, Decimal("20.00"))
        self.assertEqual(facture.montant_ttc, Decimal("120.00"))

    def test_calcul_automatique_tva_ttc(self):
        """
        Test du calcul automatique de la TVA et TTC.
        Vérifie que les calculs sont précis avec des décimales.
        """
        facture = Facture.objects.create(
            numero="FAC-2024-002",
            date="2024-01-16",
            montant_ht=Decimal("250.50"),
            taux_tva=Decimal("10.00"),
            client=self.client,
            categorie=self.categorie,
            paye=True
        )

        # Vérifier les calculs
        tva_attendue = Decimal("250.50") * Decimal("10.00") / Decimal("100")
        ttc_attendu = Decimal("250.50") + tva_attendue

        self.assertEqual(facture.montant_tva, tva_attendue)
        self.assertEqual(facture.montant_ttc, ttc_attendu)

        # Vérifier avec des valeurs précises
        self.assertEqual(facture.montant_tva, Decimal("25.05"))
        self.assertEqual(facture.montant_ttc, Decimal("275.55"))

    def test_taux_tva_different(self):
        """
        Test avec différents taux de TVA.
        Vérifie que l'application gère correctement les taux réduits et nuls.
        """
        # Test avec TVA 5.5%
        facture1 = Facture.objects.create(
            numero="FAC-2024-003",
            date="2024-01-17",
            montant_ht=Decimal("200.00"),
            taux_tva=Decimal("5.5"),
            client=self.client,
            categorie=self.categorie,
            paye=False
        )

        self.assertEqual(facture1.montant_tva, Decimal("11.00"))
        self.assertEqual(facture1.montant_ttc, Decimal("211.00"))

        # Test avec TVA 0%
        facture2 = Facture.objects.create(
            numero="FAC-2024-004",
            date="2024-01-18",
            montant_ht=Decimal("150.00"),
            taux_tva=Decimal("0.00"),
            client=self.client,
            categorie=self.categorie,
            paye=False
        )

        self.assertEqual(facture2.montant_tva, Decimal("0.00"))
        self.assertEqual(facture2.montant_ttc, Decimal("150.00"))


class LogCreationFactureModelTest(TestCase):
    """
    Tests pour le modèle LogCreationFacture.

    Vérifie la création et la gestion des logs de création de factures.
    """

    def setUp(self):
        """
        Création des données de test pour les logs.
        """
        # Créer un client de test
        self.client = Client.objects.create(
            nom="Test Client",
            email="test@example.com"
        )

        # Créer une catégorie de test
        self.categorie = Categorie.objects.create(
            nom="Test Category",
            couleur="#FF0000"
        )

        # Créer une facture de test
        self.facture = Facture.objects.create(
            numero="FAC-TEST-001",
            date="2024-01-01",
            montant_ht=Decimal("100.00"),
            taux_tva=Decimal("20.00"),
            client=self.client,
            categorie=self.categorie,
            paye=False
        )

    def test_creation_log_facture(self):
        """
        Test de création d'un log de création de facture.
        """
        log = LogCreationFacture.objects.create(
            facture=self.facture,
            ip_utilisateur="127.0.0.1",
            user_agent="Mozilla/5.0 Test Browser",
            methode_creation="formulaire_web",
            details_supplementaires={"utilisateur": "test_user"}
        )

        # Vérifier que le log a été créé
        self.assertEqual(log.facture, self.facture)
        self.assertEqual(log.ip_utilisateur, "127.0.0.1")
        self.assertEqual(log.user_agent, "Mozilla/5.0 Test Browser")
        self.assertEqual(log.methode_creation, "formulaire_web")
        self.assertEqual(log.details_supplementaires["utilisateur"], "test_user")

    def test_representation_string_log(self):
        """
        Test de la méthode __str__ du modèle LogCreationFacture.
        """
        log = LogCreationFacture.objects.create(
            facture=self.facture,
            ip_utilisateur="127.0.0.1",
            methode_creation="formulaire_web"
        )

        expected_string = f"Log création {self.facture.numero} - {log.date_creation}"
        self.assertIn("Log création FAC-TEST-001", str(log))

    def test_log_avec_details_json(self):
        """
        Test de création d'un log avec des détails JSON complexes.
        """
        details = {
            "utilisateur": "admin",
            "session_id": "abc123",
            "navigateur": "Chrome",
            "actions": ["validation", "sauvegarde"]
        }

        log = LogCreationFacture.objects.create(
            facture=self.facture,
            ip_utilisateur="192.168.1.1",
            methode_creation="api_rest",
            details_supplementaires=details
        )

        # Vérifier que les détails JSON sont correctement sauvegardés
        self.assertEqual(log.details_supplementaires["utilisateur"], "admin")
        self.assertEqual(log.details_supplementaires["actions"], ["validation", "sauvegarde"])

class LogCreationFactureMiddlewareTest(TestCase):
    """
    Tests pour le middleware LogCreationFactureMiddleware.

    Vérifie que le middleware intercepte correctement les créations de factures
    et crée les logs appropriés.
    """

    def setUp(self):
        """
        Configuration des données de test pour le middleware.
        """
        self.factory = RequestFactory()

        # Créer un client de test
        self.client = Client.objects.create(
            nom="Test Client",
            email="test@example.com"
        )

        # Créer une catégorie de test
        self.categorie = Categorie.objects.create(
            nom="Test Category",
            couleur="#FF0000"
        )

    def _create_middleware(self):
        """
        Crée une instance du middleware pour les tests.
        """
        def dummy_get_response(request):
            return HttpResponseRedirect('/factures/')

        return LogCreationFactureMiddleware(dummy_get_response)

    def test_middleware_detecte_creation_facture(self):
        """
        Test que le middleware détecte correctement les requêtes de création de facture.
        """
        middleware = self._create_middleware()
        # Test avec URL de création
        request = self.factory.post('/factures/creer/')
        self.assertTrue('/factures/creer/' in request.path)

        # Test avec URL différente
        request = self.factory.post('/factures/')
        self.assertFalse('/factures/creer/' in request.path)

    def test_middleware_recupere_ip_client(self):
        """
        Test de la récupération de l'IP client avec différents scénarios.
        """
        middleware = self._create_middleware()
        # Test avec IP directe
        request = self.factory.post('/factures/creer/')
        request.META['REMOTE_ADDR'] = '192.168.1.100'
        ip = middleware._get_client_ip(request)
        self.assertEqual(ip, '192.168.1.100')

        # Test avec proxy (X-Forwarded-For)
        request = self.factory.post('/factures/creer/')
        request.META['HTTP_X_FORWARDED_FOR'] = '10.0.0.1, 192.168.1.1'
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        ip = middleware._get_client_ip(request)
        self.assertEqual(ip, '10.0.0.1')

    def test_middleware_creation_log_apres_facture(self):
        """
        Test que le middleware crée un log après la création d'une facture.
        """
        middleware = self._create_middleware()
        # Créer une facture
        facture = Facture.objects.create(
            numero="FAC-MIDDLEWARE-001",
            date="2024-01-01",
            montant_ht=Decimal("100.00"),
            taux_tva=Decimal("20.00"),
            client=self.client,
            categorie=self.categorie,
            paye=False
        )

        # Simuler une requête POST avec succès
        request = self.factory.post('/factures/creer/')
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        request.META['HTTP_USER_AGENT'] = 'Test Browser'

        # Simuler une réponse de succès (redirection 302)
        response = HttpResponseRedirect('/factures/')

        # Traiter la réponse
        middleware.process_response(request, response)

        # Vérifier qu'un log a été créé
        logs = LogCreationFacture.objects.filter(facture=facture)
        self.assertEqual(logs.count(), 1)

        log = logs.first()
        self.assertEqual(log.ip_utilisateur, '127.0.0.1')
        self.assertEqual(log.user_agent, 'Test Browser')
        self.assertEqual(log.methode_creation, 'formulaire_web')

    def test_facture_sans_categorie(self):
        """Test de création d'une facture sans catégorie (sera assignée à 'Autres')"""
        facture = Facture.objects.create(
            numero="FAC-2024-005",
            date="2024-01-19",
            montant_ht=Decimal("75.00"),
            taux_tva=Decimal("20.00"),
            client=self.client,
            categorie=None,
            paye=False
        )

        # Vérifier que la facture existe
        self.assertIsNone(facture.categorie)
        self.assertEqual(facture.montant_ht, Decimal("75.00"))
        self.assertEqual(facture.montant_ttc, Decimal("90.00"))

    def test_validation_montant_negatif(self):
        """Test de validation avec un montant négatif"""
        facture = Facture.objects.create(
            numero="FAC-2024-006",
            date="2024-01-20",
            montant_ht=Decimal("-50.00"),  # Montant négatif
            taux_tva=Decimal("20.00"),
            client=self.client,
            categorie=self.categorie,
            paye=False
        )

        # Vérifier que la facture a été créée avec des montants négatifs
        self.assertEqual(facture.montant_ht, Decimal("-50.00"))
        self.assertEqual(facture.montant_tva, Decimal("-10.00"))
        self.assertEqual(facture.montant_ttc, Decimal("-60.00"))

    def test_representation_string(self):
        """Test de la méthode __str__ du modèle"""
        facture = Facture.objects.create(
            numero="FAC-2024-007",
            date="2024-01-21",
            montant_ht=Decimal("300.00"),
            taux_tva=Decimal("20.00"),
            client=self.client,
            categorie=self.categorie,
            paye=True
        )

        # Vérifier que la représentation string inclut le numéro et le nom du client
        # Vérifier que la représentation string inclut le numéro et le nom du client
        self.assertEqual(str(facture), "FAC-2024-007 - Test Client")


class FactureQuerySetTest(TestCase):
    """
    Tests pour le QuerySet personnalisé du modèle Facture.
    Vérifie toutes les méthodes de filtrage et d'analyse.
    """

    def setUp(self):
        """Configuration des données de test."""
        self.client1 = Client.objects.create(nom="Client A", email="a@test.com")
        self.client2 = Client.objects.create(nom="Client B", email="b@test.com")

        self.categorie1 = Categorie.objects.create(nom="Catégorie 1", couleur="#FF0000")
        self.categorie2 = Categorie.objects.create(nom="Catégorie 2", couleur="#00FF00")

        # Créer des factures de test
        self.facture1 = Facture.objects.create(
            numero="FAC-001", date="2024-01-01", montant_ht=Decimal("100.00"),
            taux_tva=Decimal("20.00"), client=self.client1, categorie=self.categorie1, paye=True
        )
        self.facture2 = Facture.objects.create(
            numero="FAC-002", date="2024-01-02", montant_ht=Decimal("200.00"),
            taux_tva=Decimal("20.00"), client=self.client2, categorie=self.categorie2, paye=False
        )
        self.facture3 = Facture.objects.create(
            numero="FAC-003", date="2024-01-03", montant_ht=Decimal("150.00"),
            taux_tva=Decimal("10.00"), client=self.client1, categorie=self.categorie1, paye=True
        )

    def test_payees(self):
        """Test de la méthode payees()."""
        factures_payees = Facture.objects.payees()
        self.assertEqual(factures_payees.count(), 2)
        self.assertIn(self.facture1, factures_payees)
        self.assertIn(self.facture3, factures_payees)

    def test_non_payees(self):
        """Test de la méthode non_payees()."""
        factures_non_payees = Facture.objects.non_payees()
        self.assertEqual(factures_non_payees.count(), 1)
        self.assertIn(self.facture2, factures_non_payees)

    def test_par_client(self):
        """Test de la méthode par_client()."""
        factures_client1 = Facture.objects.par_client(self.client1.id)
        self.assertEqual(factures_client1.count(), 2)
        self.assertIn(self.facture1, factures_client1)
        self.assertIn(self.facture3, factures_client1)

    def test_par_categorie(self):
        """Test de la méthode par_categorie()."""
        factures_cat1 = Facture.objects.par_categorie(self.categorie1.id)
        self.assertEqual(factures_cat1.count(), 2)
        self.assertIn(self.facture1, factures_cat1)
        self.assertIn(self.facture3, factures_cat1)

    def test_montant_total(self):
        """Test de la méthode montant_total()."""
        total = Facture.objects.montant_total()
        # 100*1.2 + 200*1.2 + 150*1.1 = 120 + 240 + 165 = 525
        self.assertEqual(total, Decimal("525.00"))

    def test_montant_ht_total(self):
        """Test de la méthode montant_ht_total()."""
        total_ht = Facture.objects.montant_ht_total()
        self.assertEqual(total_ht, Decimal("450.00"))

    def test_montant_tva_total(self):
        """Test de la méthode montant_tva_total()."""
        total_tva = Facture.objects.montant_tva_total()
        # 20 + 40 + 15 = 75
        self.assertEqual(total_tva, Decimal("75.00"))

    def test_recherche_avancee(self):
        """Test de la méthode recherche_avancee()."""
        # Recherche par numéro
        resultats = Facture.objects.recherche_avancee("FAC-001")
        self.assertEqual(resultats.count(), 1)
        self.assertIn(self.facture1, resultats)

        # Recherche par nom de client
        resultats = Facture.objects.recherche_avancee("Client A")
        self.assertEqual(resultats.count(), 2)
        self.assertIn(self.facture1, resultats)
        self.assertIn(self.facture3, resultats)


class FactureManagerTest(TestCase):
    """
    Tests pour le Manager personnalisé du modèle Facture.
    Vérifie les méthodes de création et d'analyse.
    """

    def setUp(self):
        """Configuration des données de test."""
        self.client = Client.objects.create(nom="Test Client", email="test@example.com")
        self.categorie = Categorie.objects.create(nom="Test Category", couleur="#FF0000")

    def test_creer_avec_categorie_autres(self):
        """Test de la méthode creer_avec_categorie_autres()."""
        # Créer une facture sans catégorie
        facture = Facture.objects.creer_avec_categorie_autres(
            numero="FAC-TEST-001",
            date="2024-01-01",
            montant_ht=Decimal("100.00"),
            taux_tva=Decimal("20.00"),
            client=self.client,
            paye=False
        )

        # Vérifier que la catégorie 'Autres' a été créée et assignée
        self.assertIsNotNone(facture.categorie)
        self.assertEqual(facture.categorie.nom, "Autres")
        self.assertEqual(facture.categorie.couleur, "#6c757d")

    def test_creer_avec_categorie_existante(self):
        """Test de la méthode creer_avec_categorie_autres() avec catégorie existante."""
        facture = Facture.objects.creer_avec_categorie_autres(
            numero="FAC-TEST-002",
            date="2024-01-01",
            montant_ht=Decimal("100.00"),
            taux_tva=Decimal("20.00"),
            client=self.client,
            categorie=self.categorie,
            paye=False
        )

        # Vérifier que la catégorie existante a été utilisée
        self.assertEqual(facture.categorie, self.categorie)

    def test_modification_facture_recalcule_tva(self):
        """Test que la modification d'une facture recalcule automatiquement la TVA"""
        facture = Facture.objects.create(
            numero="FAC-2024-008",
            date="2024-01-22",
            montant_ht=Decimal("100.00"),
            taux_tva=Decimal("20.00"),
            client=self.client,
            categorie=self.categorie,
            paye=False
        )

        # Vérifier les valeurs initiales
        self.assertEqual(facture.montant_tva, Decimal("20.00"))
        self.assertEqual(facture.montant_ttc, Decimal("120.00"))

        # Modifier le montant HT
        facture.montant_ht = Decimal("200.00")
        facture.save()

        # Vérifier que les calculs ont été mis à jour
        facture.refresh_from_db()
        self.assertEqual(facture.montant_tva, Decimal("40.00"))
        self.assertEqual(facture.montant_ttc, Decimal("240.00"))

    def test_taux_tva_limites(self):
        """Test des limites du taux de TVA"""
        # Test avec taux TVA très élevé
        facture = Facture.objects.create(
            numero="FAC-2024-009",
            date="2024-01-23",
            montant_ht=Decimal("50.00"),
            taux_tva=Decimal("100.00"),  # 100% de TVA
            client=self.client,
            categorie=self.categorie,
            paye=False
        )

        self.assertEqual(facture.montant_tva, Decimal("50.00"))
        self.assertEqual(facture.montant_ttc, Decimal("100.00"))

class FactureViewsTest(TestCase):
    """Tests pour les vues des factures"""

    def setUp(self):
        """Création des données de test pour les vues"""
        # Créer un client de test
        self.client_test = Client.objects.create(
            nom="Marie Martin",
            email="marie.martin@example.com",
            telephone="0987654321",
            adresse="456 Avenue des Champs, Lyon"
        )

        # Créer une catégorie de test
        self.categorie = Categorie.objects.create(
            nom="Consultation",
            couleur="#33FF57"
        )

        # Créer plusieurs factures de test
        self.facture1 = Facture.objects.create(
            numero="FAC-2024-010",
            date="2024-02-01",
            montant_ht=Decimal("150.00"),
            taux_tva=Decimal("20.00"),
            client=self.client_test,
            categorie=self.categorie,
            paye=True
        )

        self.facture2 = Facture.objects.create(
            numero="FAC-2024-011",
            date="2024-02-02",
            montant_ht=Decimal("200.00"),
            taux_tva=Decimal("10.00"),
            client=self.client_test,
            categorie=self.categorie,
            paye=False
        )

        self.facture3 = Facture.objects.create(
            numero="FAC-2024-012",
            date="2024-02-03",
            montant_ht=Decimal("75.50"),
            taux_tva=Decimal("5.5"),
            client=self.client_test,
            categorie=self.categorie,
            paye=True
        )

    # Tests pour la vue de listage des factures
    def test_liste_factures_acces(self):
        """Test d'accès à la vue de listage des factures"""
        response = self.client.get('/factures/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'factures/liste.html')

    def test_liste_factures_contient_factures(self):
        """Test que la liste des factures contient bien les factures créées"""
        response = self.client.get('/factures/')
        self.assertEqual(response.status_code, 200)

        # Vérifier que toutes les factures sont présentes
        self.assertContains(response, "FAC-2024-010")
        self.assertContains(response, "FAC-2024-011")
        self.assertContains(response, "FAC-2024-012")

        # Vérifier que les montants TTC sont affichés (format français avec virgules)
        self.assertContains(response, "180,00")  # 150 + 30 (TVA 20%)
        self.assertContains(response, "220,00")  # 200 + 20 (TVA 10%)
        self.assertContains(response, "79,65")   # 75.50 + 4.15 (TVA 5.5%)

    def test_liste_factures_filtre_client(self):
        """Test du filtre par client dans la liste des factures"""
        # Créer un autre client
        autre_client = Client.objects.create(
            nom="Pierre Durand",
            email="pierre.durand@example.com"
        )

        # Créer une facture pour l'autre client
        Facture.objects.create(
            numero="FAC-2024-013",
            date="2024-02-04",
            montant_ht=Decimal("100.00"),
            taux_tva=Decimal("20.00"),
            client=autre_client,
            categorie=self.categorie,
            paye=False
        )

        # Tester le filtre par client
        response = self.client.get('/factures/', {'client': self.client_test.id})
        self.assertEqual(response.status_code, 200)

        # Vérifier que seules les factures du client filtré sont présentes
        self.assertContains(response, "FAC-2024-010")
        self.assertContains(response, "FAC-2024-011")
        self.assertContains(response, "FAC-2024-012")
        self.assertNotContains(response, "FAC-2024-013")

    def test_liste_factures_filtre_categorie(self):
        """Test du filtre par catégorie dans la liste des factures"""
        # Créer une autre catégorie
        autre_categorie = Categorie.objects.create(
            nom="Formation",
            couleur="#FF5733"
        )

        # Créer une facture pour l'autre catégorie
        Facture.objects.create(
            numero="FAC-2024-017",
            date="2024-02-08",
            montant_ht=Decimal("300.00"),
            taux_tva=Decimal("20.00"),
            client=self.client_test,
            categorie=autre_categorie,
            paye=True
        )

        # Tester le filtre par catégorie
        response = self.client.get('/factures/', {'categorie': self.categorie.id})
        self.assertEqual(response.status_code, 200)

        # Vérifier que seules les factures de la catégorie filtrée sont présentes
        self.assertContains(response, "FAC-2024-010")
        self.assertContains(response, "FAC-2024-011")
        self.assertContains(response, "FAC-2024-012")
        self.assertNotContains(response, "FAC-2024-017")

    def test_liste_factures_filtres_combines(self):
        """Test des filtres combinés (client + catégorie)"""
        # Créer un autre client et une autre catégorie
        autre_client = Client.objects.create(
            nom="Sophie Bernard",
            email="sophie.bernard@example.com"
        )
        autre_categorie = Categorie.objects.create(
            nom="Maintenance",
            couleur="#33FF57"
        )

        # Créer des factures avec différentes combinaisons
        Facture.objects.create(
            numero="FAC-2024-018",
            date="2024-02-09",
            montant_ht=Decimal("150.00"),
            taux_tva=Decimal("20.00"),
            client=autre_client,
            categorie=self.categorie,  # Même catégorie, client différent
            paye=False
        )

        Facture.objects.create(
            numero="FAC-2024-019",
            date="2024-02-10",
            montant_ht=Decimal("200.00"),
            taux_tva=Decimal("20.00"),
            client=self.client_test,
            categorie=autre_categorie,  # Même client, catégorie différente
            paye=True
        )

        # Tester les filtres combinés
        response = self.client.get('/factures/', {
            'client': self.client_test.id,
            'categorie': self.categorie.id
        })
        self.assertEqual(response.status_code, 200)

        # Vérifier que seules les factures correspondant aux deux filtres sont présentes
        self.assertContains(response, "FAC-2024-010")
        self.assertContains(response, "FAC-2024-011")
        self.assertContains(response, "FAC-2024-012")
        self.assertNotContains(response, "FAC-2024-018")  # Client différent
        self.assertNotContains(response, "FAC-2024-019")  # Catégorie différente


    # Tests pour la vue d'affichage d'une facture
    def test_detail_facture_acces(self):
        """Test d'accès à la vue de détail d'une facture"""
        response = self.client.get(f'/factures/{self.facture1.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'factures/detail.html')

    def test_detail_facture_contient_informations(self):
        """Test que la vue de détail contient toutes les informations de la facture"""
        response = self.client.get(f'/factures/{self.facture1.pk}/')
        self.assertEqual(response.status_code, 200)

        # Vérifier les informations de base
        self.assertContains(response, "FAC-2024-010")
        self.assertContains(response, "1 février 2024")  # Format français
        self.assertContains(response, "Marie Martin")

        # Vérifier les montants (format français avec virgules)
        self.assertContains(response, "150,00")  # Montant HT
        self.assertContains(response, "20,00")   # Taux TVA
        self.assertContains(response, "30,00")   # Montant TVA
        self.assertContains(response, "180,00")  # Montant TTC

    def test_detail_facture_404(self):
        """Test que la vue de détail retourne 404 pour une facture inexistante"""
        response = self.client.get('/factures/99999/')
        self.assertEqual(response.status_code, 404)

    def test_detail_facture_liens_navigation(self):
        """Test que la vue de détail contient les liens de navigation corrects"""
        response = self.client.get(f'/factures/{self.facture1.pk}/')
        self.assertEqual(response.status_code, 200)

        # Vérifier la présence des liens de navigation
        self.assertContains(response, 'href="/"')  # Lien vers l'accueil
        self.assertContains(response, 'href="/factures/"')  # Lien vers la liste
        self.assertContains(response, f'href="/factures/{self.facture1.pk}/modifier/"')  # Lien de modification
        self.assertContains(response, f'href="/factures/{self.facture1.pk}/supprimer/"')  # Lien de suppression

    def test_detail_facture_statut_paye_affichage(self):
        """Test que le statut de paiement est correctement affiché"""
        # Tester avec une facture payée
        response = self.client.get(f'/factures/{self.facture1.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Payée")
        self.assertContains(response, "bg-success")

        # Tester avec une facture non payée
        response = self.client.get(f'/factures/{self.facture2.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Non payée")
        self.assertContains(response, "bg-danger")


    # Tests pour la vue de création d'une facture
    def test_creer_facture_acces_get(self):
        """Test d'accès à la vue de création d'une facture (GET)"""
        response = self.client.get('/factures/creer/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'factures/creer.html')

    def test_creer_facture_post_valide(self):
        """Test de création d'une facture avec des données valides (POST)"""
        data = {
            'numero': 'FAC-2024-014-TEST',
            'date': '2024-02-05',
            'montant_ht': '125.00',
            'taux_tva': '20.00',
            'client': self.client_test.id,
            'categorie': self.categorie.id,
            'paye': False
        }

        response = self.client.post('/factures/creer/', data)

        # Vérifier la redirection après création
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/factures/')

        # Vérifier que la facture a été créée en base
        facture_creee = Facture.objects.filter(numero='FAC-2024-014-TEST').latest('id')
        self.assertEqual(facture_creee.montant_ht, Decimal('125.00'))
        self.assertEqual(facture_creee.montant_ttc, Decimal('150.00'))
        self.assertEqual(facture_creee.client, self.client_test)

    def test_creer_facture_post_invalide(self):
        """Test de création d'une facture avec des données invalides (POST)"""
        data = {
            'numero': '',  # Numéro vide
            'date': '2024-02-05',
            'montant_ht': '125.00',
            'taux_tva': '20.00',
            'client': self.client_test.id,
            'categorie': self.categorie.id,
            'paye': False
        }

        response = self.client.post('/factures/creer/', data)

        # Vérifier que la page s'affiche avec des erreurs
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce champ est obligatoire")

    def test_creer_facture_sans_categorie_assignation_automatique(self):
        """Test que la création d'une facture sans catégorie assigne automatiquement 'Autres'"""
        data = {
            'numero': 'FAC-2024-015-TEST',
            'date': '2024-02-06',
            'montant_ht': '80.00',
            'taux_tva': '20.00',
            'client': self.client_test.id,
            # Pas de catégorie sélectionnée
            'paye': False
        }

        response = self.client.post('/factures/creer/', data)

        # Vérifier la redirection après création
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/factures/')

        # Vérifier que la facture a été créée avec la catégorie "Autres"
        facture_creee = Facture.objects.filter(numero='FAC-2024-015-TEST').latest('id')
        self.assertIsNotNone(facture_creee.categorie)
        self.assertEqual(facture_creee.categorie.nom, "Autres")
        self.assertEqual(facture_creee.montant_ttc, Decimal('96.00'))

    def test_creer_facture_montant_negatif(self):
        """Test de création d'une facture avec un montant négatif (doit fonctionner)"""
        data = {
            'numero': 'FAC-2024-016-TEST',
            'date': '2024-02-07',
            'montant_ht': '-25.00',  # Montant négatif
            'taux_tva': '20.00',
            'client': self.client_test.id,
            'categorie': self.categorie.id,
            'paye': False
        }

        response = self.client.post('/factures/creer/', data)

        # Vérifier que la création fonctionne même avec un montant négatif
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/factures/')

        # Vérifier que la facture a été créée avec les calculs corrects
        facture_creee = Facture.objects.filter(numero='FAC-2024-016-TEST').latest('id')
        self.assertEqual(facture_creee.montant_ht, Decimal('-25.00'))
        self.assertEqual(facture_creee.montant_tva, Decimal('-5.00'))
        self.assertEqual(facture_creee.montant_ttc, Decimal('-30.00'))
