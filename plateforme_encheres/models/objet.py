"""
models/objet.py
Classe Objet — hérite de EntiteBase.

Bloc 3 — POO : encapsulation, héritage, modularité.
"""

from models.base import EntiteBase

STATUTS_VALIDES: set = {"en_attente", "actif", "vendu", "non_vendu"}


class Objet(EntiteBase):
    """Représente un objet mis en vente sur la plateforme.

    Hérite de EntiteBase : identifiant unique et interface to_dict().

    Attributs:
        id (int)              : Identifiant unique (hérité).
        __titre (str)         : Titre de l'objet (encapsulé).
        __description (str)   : Description courte (encapsulé).
        __prix_depart (float) : Prix de départ de l'enchère (encapsulé).
        __vendeur (str)       : Email du vendeur (encapsulé).
        duree_tours (int)     : Durée en nombre de tours.
        __statut (str)        : État courant (encapsulé).
    """

    def __init__(
        self,
        titre: str,
        description: str,
        prix_depart: float,
        vendeur: str,
        duree_tours: int = 1,
    ) -> None:
        super().__init__()  # Appel EntiteBase → attribue self.id

        # Attributs encapsulés (privés)
        self.__titre: str = titre
        self.__description: str = description
        self.__prix_depart: float = prix_depart
        self.__vendeur: str = vendeur
        self.__statut: str = "en_attente"

        # Attribut public
        self.duree_tours: int = duree_tours

    # ── Propriétés (encapsulation) ───────────────────────────────────────────

    @property
    def titre(self) -> str:
        return self.__titre

    @property
    def description(self) -> str:
        return self.__description

    @property
    def prix_depart(self) -> float:
        return self.__prix_depart

    @property
    def vendeur(self) -> str:
        return self.__vendeur

    @property
    def statut(self) -> str:
        return self.__statut

    # ── Méthodes métier ──────────────────────────────────────────────────────

    def mettre_en_vente(self) -> bool:
        """Publie l'objet — passe le statut à 'actif'.

        Returns:
            True si la mise en vente a réussi, False sinon.

        Example:
            >>> o = Objet("Vase", "Ancien", 500.0, "alice@mail.com")
            >>> o.mettre_en_vente()
            True
            >>> o.statut
            'actif'
        """
        if self.__statut == "en_attente":
            self.__statut = "actif"
            return True
        return False

    def est_disponible(self) -> bool:
        """Retourne True si l'objet accepte encore des mises.

        Example:
            >>> o = Objet("Vase", "Ancien", 500.0, "alice@mail.com")
            >>> o.est_disponible()
            False
            >>> o.mettre_en_vente()
            True
            >>> o.est_disponible()
            True
        """
        return self.__statut == "actif"

    def marquer_vendu(self) -> None:
        """Marque l'objet comme vendu."""
        self.__statut = "vendu"

    def marquer_non_vendu(self) -> None:
        """Marque l'objet comme non vendu (aucune mise reçue à la clôture)."""
        self.__statut = "non_vendu"

    # ── Persistance JSON ─────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Sérialise l'objet en dict pour la sauvegarde JSON.

        Example:
            >>> o = Objet("Vase", "Ancien", 500.0, "alice@mail.com")
            >>> o.to_dict()["titre"]
            'Vase'
        """
        return {
            "id": self.id,
            "titre": self.__titre,
            "description": self.__description,
            "prix_depart": self.__prix_depart,
            "vendeur": self.__vendeur,
            "duree_tours": self.duree_tours,
            "statut": self.__statut,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Objet":
        """Recrée un Objet depuis un dict JSON."""
        o = cls(
            data["titre"],
            data["description"],
            data["prix_depart"],
            data["vendeur"],
            data.get("duree_tours", 1),
        )
        o._Objet__statut = data["statut"]
        o.id = data["id"]
        if data["id"] >= cls._compteur_id:
            cls._compteur_id = data["id"]
        return o

    def __repr__(self) -> str:
        return (
            f"Objet(id={self.id}, titre={self.__titre!r}, "
            f"statut={self.__statut!r}, prix_depart={self.__prix_depart} FCFA)"
        )
