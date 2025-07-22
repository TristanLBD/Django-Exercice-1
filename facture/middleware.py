"""
Middleware pour enregistrer les logs de création de factures.

Ce middleware intercepte uniquement les requêtes POST vers les vues de création de factures
et enregistre automatiquement un log en base de données.
"""
from django.utils.deprecation import MiddlewareMixin
from .models import LogCreationFacture, Facture


class LogCreationFactureMiddleware(MiddlewareMixin):
    """
    Middleware qui enregistre automatiquement les logs de création de factures.
    """

    def process_response(self, request, response):
        """
        Traite la réponse sortante.
        Vérifie si une facture a été créée et enregistre le log si nécessaire.
        """
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


