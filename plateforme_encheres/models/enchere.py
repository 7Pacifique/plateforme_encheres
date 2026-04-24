"""
models/enchere.py
Classe Enchere — hérite de EntiteBase.

Bloc 3 — POO : encapsulation, héritage, modularité.
"""

from datetime import datetime
from models.base import EntiteBase


class Enchere(EntiteBase):
    """Gère le cycle de vie d'une enchère sur un objet.

    Hérite de EntiteBase : identifiant unique et interface to_dict().

    Attributs:
        id (int)                          : Identifiant unique (hérité).
        __id_objet (int)                  : ID de l'objet mis en enchère (encapsulé).
        __montant_actuel (float)          : Meilleure mise en cours (encapsulé).
        __meilleur_encherisseur (str|None): Email du meilleur enchérisseur (encapsulé).
        __date_fin (str)                  : Horodatage ISO de clôture prévue (encapsulé).
        __est_cloturee (bool)             : True si l'enchère est terminée (encapsulé).
        historique_mises (list)           : List de tuples (email, montant, horodatage).
    """

    def __init__(self, id_objet: int, prix_depart: float, date_fin: str) -> None:
        super().__init__()  # Appel EntiteBase → attribue self.id

        # Attributs encapsulés (privés)
        self.__id_objet: int = id_objet
        self.__montant_actuel: float = prix_depart
        self.__meilleur_encherisseur: str | None = None
        self.__date_fin: str = date_fin
        self.__est_cloturee: bool = False

        # Type complexe public
        self.historique_mises: list = []  # list de tuples

    # ── Propriétés (encapsulation) ───────────────────────────────────────────

    @property
    def id_objet(self) -> int:
        return self.__id_objet

    @property
    def montant_actuel(self) -> float:
        return self.__montant_actuel

    @property
    def meilleur_encherisseur(self) -> str | None:
        return self.__meilleur_encherisseur

    @property
    def date_fin(self) -> str:
        return self.__date_fin

    @property
    def est_cloturee(self) -> bool:
        return self.__est_cloturee

    # ── Méthodes métier ──────────────────────────────────────────────────────

    def placer_mise(self, email_encherisseur: str, montant: float) -> bool:
        """Enregistre une mise si elle est valide.

        Règles :
        - L'enchère ne doit pas être clôturée.
        - Le montant doit être strictement supérieur au montant actuel.

        Args:
            email_encherisseur: Email de l'enchérisseur.
            montant: Montant proposé.

        Returns:
            True si acceptée, False sinon.

        Example:
            >>> e = Enchere(1, 500.0, "2026-04-30T23:59:00")
            >>> e.placer_mise("bob@mail.com", 600.0)
            True
            >>> e.montant_actuel
            600.0
        """
        if self.__est_cloturee:
            return False
        if montant <= self.__montant_actuel:
            return False

        self.__montant_actuel = montant
        self.__meilleur_encherisseur = email_encherisseur
        horodatage = datetime.now().isoformat(timespec="seconds")
        self.historique_mises.append((email_encherisseur, montant, horodatage))
        return True

    def cloturer(self) -> dict:
        """Clôture l'enchère et retourne le résultat.

        Returns:
            dict: Résumé — gagnant, montant final, statut vendu.

        Example:
            >>> e = Enchere(1, 500.0, "2026-04-30T23:59:00")
            >>> e.placer_mise("bob@mail.com", 700.0)
            True
            >>> e.cloturer()["gagnant"]
            'bob@mail.com'
        """
        self.__est_cloturee = True
        return {
            "id_enchere": self.id,
            "id_objet": self.__id_objet,
            "gagnant": self.__meilleur_encherisseur,
            "montant_final": self.__montant_actuel,
            "vendu": self.__meilleur_encherisseur is not None,
            "nb_mises": len(self.historique_mises),
        }

    def get_gagnant(self) -> str | None:
        """Retourne l'email du gagnant, ou None si aucune mise.

        Example:
            >>> e = Enchere(1, 500.0, "2026-04-30T23:59:00")
            >>> e.get_gagnant() is None
            True
        """
        return self.__meilleur_encherisseur

    # ── Persistance JSON ─────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Sérialise l'enchère en dict pour la sauvegarde JSON."""
        return {
            "id": self.id,
            "id_objet": self.__id_objet,
            "montant_actuel": self.__montant_actuel,
            "meilleur_encherisseur": self.__meilleur_encherisseur,
            "date_fin": self.__date_fin,
            "est_cloturee": self.__est_cloturee,
            "historique_mises": [list(m) for m in self.historique_mises],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Enchere":
        """Recrée une Enchere depuis un dict JSON."""
        e = cls(data["id_objet"], data["montant_actuel"], data["date_fin"])
        e._Enchere__meilleur_encherisseur = data["meilleur_encherisseur"]
        e._Enchere__est_cloturee = data["est_cloturee"]
        e.historique_mises = [tuple(m) for m in data.get("historique_mises", [])]
        e.id = data["id"]
        if data["id"] >= cls._compteur_id:
            cls._compteur_id = data["id"]
        return e

    def __repr__(self) -> str:
        return (
            f"Enchere(id={self.id}, objet={self.__id_objet}, "
            f"montant={self.__montant_actuel} FCFA, "
            f"cloturee={self.__est_cloturee})"
        )
