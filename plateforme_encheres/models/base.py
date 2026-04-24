"""
models/base.py
Classe de base abstraite pour toutes les entités du projet.

Bloc 3 — Héritage : Utilisateur, Objet et Enchere héritent de EntiteBase.
"""

from abc import ABC, abstractmethod


class EntiteBase(ABC):
    """Classe mère abstraite commune à toutes les entités de la plateforme.

    Fournit :
    - Un identifiant unique auto-incrémenté par classe fille.
    - Une méthode abstraite to_dict() que chaque fille doit implémenter.
    - Une méthode abstraite from_dict() pour la reconstruction depuis JSON.
    - Un __repr__() de base.
    """

    _compteur_id: int = 0  # Compteur propre à chaque classe fille (héritage)

    def __init__(self) -> None:
        """Initialise l'entité en lui attribuant un identifiant unique."""
        # Chaque classe fille incrémente son propre compteur
        self.__class__._compteur_id += 1
        self.id: int = self.__class__._compteur_id

    @abstractmethod
    def to_dict(self) -> dict:
        """Sérialise l'entité en dictionnaire pour la sauvegarde JSON.

        Returns:
            dict: Représentation sérialisable en JSON.
        """

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "EntiteBase":
        """Recrée l'entité depuis un dictionnaire chargé depuis JSON.

        Args:
            data: Dictionnaire issu du fichier JSON.

        Returns:
            Instance reconstruite de la classe fille.
        """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
