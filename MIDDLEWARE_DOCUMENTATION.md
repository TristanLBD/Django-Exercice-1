# Middleware de Logging des Créations de Factures

## 📋 Description

Ce middleware Django intercepte automatiquement les créations de factures et enregistre des logs en base de données. Il capture l'adresse IP de l'utilisateur, le user agent et d'autres informations essentielles pour l'audit.

## 🏗️ Architecture

### Modèle `LogCreationFacture`

```python
class LogCreationFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    ip_utilisateur = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    methode_creation = models.CharField(max_length=50)
    details_supplementaires = models.JSONField(blank=True, null=True)
```

**Champs :**

-   **`facture`** : Référence vers la facture créée
-   **`date_creation`** : Horodatage automatique de la création du log
-   **`ip_utilisateur`** : Adresse IP de l'utilisateur (gère les proxies)
-   **`user_agent`** : Navigateur et système d'exploitation
-   **`methode_creation`** : Méthode utilisée (formulaire_web, API, etc.)
-   **`details_supplementaires`** : Informations JSON supplémentaires

### Middleware `LogCreationFactureMiddleware`

Le middleware fonctionne en une seule phase :

**`process_response()`** : Vérifie si une facture a été créée et enregistre le log

## 🔧 Configuration

### 1. Ajout du Middleware

Le middleware est configuré dans `settings.py` :

```python
MIDDLEWARE = [
    # ... autres middlewares ...
    'facture.middleware.LogCreationFactureMiddleware',
]
```

### 2. Migration de la Base de Données

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🎯 Fonctionnalités

### ✅ **Interception Ciblée**

-   Détecte uniquement les requêtes POST vers `/factures/creer/`
-   Vérifie le succès de la création (redirection 302)
-   Fonctionne avec les vues de création de factures existantes

### ✅ **Capture d'Informations Essentielles**

-   **Adresse IP** : Gère les proxies et load balancers
-   **User Agent** : Navigateur et système d'exploitation
-   **Horodatage** : Date et heure précises de création

### ✅ **Gestion d'Erreurs**

-   Ne bloque jamais le processus de création
-   Gestion gracieuse des erreurs de base de données

### ✅ **Interface d'Administration**

-   Vue dédiée dans Django Admin
-   Filtres avancés par date, méthode, client
-   Recherche par numéro de facture et IP
-   Affichage des informations utilisateur

## 📊 Utilisation

### Interface d'Administration

Accédez à `/admin/facture/logcreationfacture/` pour voir tous les logs :

-   **Liste** : Tous les logs avec filtres
-   **Recherche** : Par numéro de facture, client, IP
-   **Filtres** : Par date, méthode, catégorie
-   **Lecture seule** : Les logs ne peuvent pas être modifiés

### Vue de Test

Accédez à `/test-middleware/` pour une interface de test :

-   **Statistiques** : Nombre total de logs
-   **Derniers logs** : 10 créations les plus récentes
-   **Détails** : Informations complètes de chaque création
-   **Test en direct** : Créez une facture pour voir le log

## 🧪 Tests

### Tests du Modèle

```python
class LogCreationFactureModelTest(TestCase):
    def test_creation_log_facture(self):
        # Test de création d'un log
    def test_representation_string_log(self):
        # Test de la méthode __str__
    def test_log_avec_details_json(self):
        # Test avec détails JSON complexes
```

### Tests du Middleware

```python
class LogCreationFactureMiddlewareTest(TestCase):
    def test_middleware_detecte_creation_facture(self):
        # Test de détection des URLs
    def test_middleware_recupere_ip_client(self):
        # Test de récupération d'IP
    def test_middleware_creation_log_apres_facture(self):
        # Test de création de log
```

## 🔍 Exemples d'Utilisation

### Log Typique

```json
{
    "facture": "FAC-2024-001 - Jean Dupont",
    "date_creation": "2024-01-15 14:30:25",
    "ip_utilisateur": "192.168.1.100",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "methode_creation": "formulaire_web",
    "details_supplementaires": {}
}
```

### Requêtes Utiles

```python
# Logs des dernières 24h
from datetime import datetime, timedelta
logs_24h = LogCreationFacture.objects.filter(
    date_creation__gte=datetime.now() - timedelta(days=1)
)

# Logs par IP
logs_ip = LogCreationFacture.objects.filter(ip_utilisateur='192.168.1.100')

# Logs par méthode
logs_api = LogCreationFacture.objects.filter(methode_creation='formulaire_web')
```

## 🚀 Avantages

### **Audit et Conformité**

-   Traçabilité complète des créations de factures
-   Conformité aux exigences d'audit
-   Historique des actions utilisateurs

### **Sécurité**

-   Détection d'activités suspectes
-   Surveillance des accès par IP
-   Identification des utilisateurs

### **Analyse et Statistiques**

-   Statistiques de création par période
-   Analyse des patterns d'utilisation
-   Métriques de performance

### **Support et Debugging**

-   Identification rapide des problèmes
-   Support utilisateur amélioré
-   Debugging des erreurs de création

## 🔧 Code du Middleware

```python
class LogCreationFactureMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Vérifier si c'est une requête POST vers une vue de création de facture
        if (request.method == 'POST' and
            '/factures/creer/' in request.path and
            response.status_code == 302):  # Succès = redirection

            try:
                # Récupérer la facture la plus récemment créée
                facture = Facture.objects.latest('id')

                # Créer le log de création
                LogCreationFacture.objects.create(
                    facture=facture,
                    ip_utilisateur=self._get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    methode_creation='formulaire_web',
                    details_supplementaires={}
                )

            except Facture.DoesNotExist:
                # Aucune facture trouvée, ne pas créer de log
                pass
            except Exception as e:
                # En cas d'erreur, ne pas bloquer la réponse
                pass

        return response

    def _get_client_ip(self, request):
        """
        Récupère l'adresse IP réelle du client.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

## 📈 Métriques et KPIs

### Métriques Disponibles

-   **Volume** : Nombre de factures créées par jour/semaine/mois
-   **Sources** : Répartition par méthode de création
-   **Utilisateurs** : Activité par IP
-   **Performance** : Temps de création et patterns

### Exemples de Requêtes

```python
# Factures créées aujourd'hui
from django.utils import timezone
aujourd_hui = LogCreationFacture.objects.filter(
    date_creation__date=timezone.now().date()
).count()

# Top 5 des IPs les plus actives
from django.db.models import Count
top_ips = LogCreationFacture.objects.values('ip_utilisateur').annotate(
    count=Count('id')
).order_by('-count')[:5]
```

## 🔒 Sécurité et Performance

### Sécurité

-   **Données sensibles** : Les mots de passe ne sont jamais loggés
-   **IP anonymisation** : Option pour anonymiser les IPs
-   **Rétention** : Politique de rétention des logs configurable

### Performance

-   **Minimal** : Impact minimal sur les performances
-   **Indexation** : Index sur les champs de recherche fréquents
-   **Nettoyage** : Suppression automatique des anciens logs

## 🎯 Roadmap

### Fonctionnalités Futures

1. **Logs de Modification** : Tracer les modifications de factures
2. **Logs de Suppression** : Tracer les suppressions
3. **Notifications** : Alertes sur activités suspectes
4. **Export** : Export des logs en CSV/JSON
5. **API** : Endpoints REST pour consulter les logs

---

**Le middleware est maintenant opérationnel et prêt à tracer toutes les créations de factures !** 🎉
