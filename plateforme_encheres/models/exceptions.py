"""
models/exceptions.py
Exceptions personnalisées de la Plateforme d'Enchères.

Bloc 5 — Gestion des erreurs et robustesse.
"""


class PlateForme_Erreur(Exception):
    """Classe de base pour toutes les exceptions du projet."""


class EmailDejaUtiliseError(PlateForme_Erreur):
    """Levée quand on tente de s'inscrire avec un email déjà pris."""


class IdentifiantsInvalidesError(PlateForme_Erreur):
    """Levée quand email ou mot de passe est incorrect à la connexion."""


class ChampVideError(PlateForme_Erreur):
    """Levée quand un champ obligatoire est vide."""


class PrixInvalideError(PlateForme_Erreur):
    """Levée quand le prix de départ est négatif ou nul."""


class SoldeInsuffisantError(PlateForme_Erreur):
    """Levée quand le solde est insuffisant pour placer une mise."""


class VendeurEncheritError(PlateForme_Erreur):
    """Levée quand un vendeur tente de miser sur son propre objet."""


class MiseTropBasseError(PlateForme_Erreur):
    """Levée quand la mise est inférieure ou égale à l'offre actuelle."""


class EnchereIntrouvableError(PlateForme_Erreur):
    """Levée quand l'enchère demandée n'existe pas."""


class EnchereClotureeError(PlateForme_Erreur):
    """Levée quand on tente une action sur une enchère déjà clôturée."""
