"""
models/utilisateur.py
Classe Utilisateur — hérite de EntiteBase.

Bloc 3 — POO : encapsulation, héritage, modularité.
"""

from models.base import EntiteBase


class Utilisateur(EntiteBase):
    """Représente un utilisateur de la plateforme d'enchères.

    Hérite de EntiteBase : récupère l'identifiant unique et to_dict().

    Attributs:
        id (int)                    : Identifiant unique (hérité).
        __nom (str)                 : Nom d'utilisateur (encapsulé).
        __email (str)               : Adresse email (encapsulé).
        __mot_de_passe (str)        : Mot de passe (encapsulé).
        __solde (float)             : Solde virtuel en FCFA (encapsulé).
        historique (list)           : Liste de tuples — transactions effectuées.
        objets_en_vente (list)      : IDs des objets déposés par l'utilisateur.
        encheres_participees (set)  : IDs des enchères rejointes (sans doublons).
    """

    SOLDE_INITIAL: float = 10_000.0  # 10 000 FCFA virtuels à l'inscription

    def __init__(self, nom: str, email: str, mot_de_passe: str) -> None:
        super().__init__()  # Appel EntiteBase → attribue self.id

        # Attributs encapsulés (privés)
        self.__nom: str = nom
        self.__email: str = email
        self.__mot_de_passe: str = mot_de_passe
        self.__solde: float = self.SOLDE_INITIAL

        # Types complexes
        self.historique: list = []              # list de tuples
        self.objets_en_vente: list = []         # list d'IDs
        self.encheres_participees: set = set()  # set d'IDs

    # ── Propriétés (encapsulation) ───────────────────────────────────────────

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def email(self) -> str:
        return self.__email

    @property
    def solde(self) -> float:
        return self.__solde

    # ── Authentification ─────────────────────────────────────────────────────

    @staticmethod
    def inscrire(nom: str, email: str, mot_de_passe: str) -> "Utilisateur":
        """Crée et retourne un nouvel utilisateur avec solde initial.

        Example:
            >>> u = Utilisateur.inscrire("Alice", "alice@mail.com", "1234")
            >>> u.solde
            10000.0
        """
        return Utilisateur(nom, email, mot_de_passe)

    def se_connecter(self, email: str, mot_de_passe: str) -> bool:
        """Vérifie les identifiants. Retourne True si corrects.

        Example:
            >>> u = Utilisateur("Alice", "alice@mail.com", "1234")
            >>> u.se_connecter("alice@mail.com", "1234")
            True
            >>> u.se_connecter("alice@mail.com", "wrong")
            False
        """
        return self.__email == email and self.__mot_de_passe == mot_de_passe

    # ── Gestion du solde ─────────────────────────────────────────────────────

    def crediter(self, montant: float, motif: str = "") -> None:
        """Crédite le solde et enregistre la transaction.

        Example:
            >>> u = Utilisateur("Alice", "alice@mail.com", "1234")
            >>> u.crediter(500.0, "Vente objet #2")
            >>> u.solde
            10500.0
        """
        self.__solde += montant
        self.historique.append(("credit", montant, motif))

    def debiter(self, montant: float, motif: str = "") -> bool:
        """Débite le solde si fonds suffisants. Retourne True si réussi.

        Example:
            >>> u = Utilisateur("Alice", "alice@mail.com", "1234")
            >>> u.debiter(3000.0, "Mise enchère #1")
            True
            >>> u.debiter(99999.0, "Trop cher")
            False
        """
        if montant > self.__solde:
            return False
        self.__solde -= montant
        self.historique.append(("debit", montant, motif))
        return True

    def rejoindre_enchere(self, enchere_id: int) -> None:
        """Enregistre la participation à une enchère (set = pas de doublons)."""
        self.encheres_participees.add(enchere_id)

    # ── Persistance JSON ─────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Sérialise l'utilisateur en dict pour la sauvegarde JSON.

        Example:
            >>> u = Utilisateur("Alice", "alice@mail.com", "1234")
            >>> u.to_dict()["email"]
            'alice@mail.com'
        """
        return {
            "id": self.id,
            "nom": self.__nom,
            "email": self.__email,
            "mot_de_passe": self.__mot_de_passe,
            "solde": self.__solde,
            "historique": [list(t) for t in self.historique],
            "objets_en_vente": self.objets_en_vente,
            "encheres_participees": list(self.encheres_participees),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Utilisateur":
        """Recrée un Utilisateur depuis un dict JSON."""
        u = cls(data["nom"], data["email"], data["mot_de_passe"])
        u._Utilisateur__solde = data["solde"]
        u.historique = [tuple(t) for t in data.get("historique", [])]
        u.objets_en_vente = data.get("objets_en_vente", [])
        u.encheres_participees = set(data.get("encheres_participees", []))
        u.id = data["id"]
        if data["id"] >= cls._compteur_id:
            cls._compteur_id = data["id"]
        return u

    def __repr__(self) -> str:
        return (
            f"Utilisateur(id={self.id}, nom={self.__nom!r}, "
            f"solde={self.__solde} FCFA)"
        )
