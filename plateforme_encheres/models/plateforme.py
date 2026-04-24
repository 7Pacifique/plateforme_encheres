"""
models/plateforme.py
Classe Plateforme — (n'hérite pas de EntiteBase).

Bloc 3 — POO : modularité, coordination des classes.
Bloc 4 — Persistance JSON : charger_donnees() / sauvegarder().
Bloc 6 — Interface CLI : lancer() / afficher_objets()
"""

import json
import os
from datetime import datetime

from models.utilisateur import Utilisateur
from models.objet import Objet
from models.enchere import Enchere

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FICHIER_UTILISATEURS = os.path.join(DATA_DIR, "utilisateurs.json")
FICHIER_OBJETS = os.path.join(DATA_DIR, "objets.json")
FICHIER_ENCHERES = os.path.join(DATA_DIR, "encheres.json")


class Plateforme:
    """Orchestre l'ensemble de la plateforme d'enchères.

    Attributs:
        utilisateurs (dict)                       : email -> Utilisateur.
        objets (dict)                             : id -> Objet.
        encheres (dict)                           : id -> Enchere.
        encheres_actives (list)                   : IDs des enchères en cours.
        categories (set)                          : Catégories disponibles.
        utilisateur_connecte (Utilisateur | None) : Session active.
    """

    def __init__(self) -> None:
        """Initialise la plateforme et charge les données existantes."""
        self.utilisateurs: dict = {}
        self.objets: dict = {}
        self.encheres: dict = {}
        self.encheres_actives: list = []
        self.categories: set = {"electronique", "mode", "art", "livres", "divers"}
        self.utilisateur_connecte: Utilisateur | None = None
        self.charger_donnees()

    # ── Persistance JSON ─────────────────────────────────────────────────────

    def charger_donnees(self) -> None:
        """Charge les données depuis les fichiers JSON.

        Crée les fichiers vides automatiquement s'ils sont absents.
        Affiche un message clair si un fichier est corrompu.
        """
        os.makedirs(DATA_DIR, exist_ok=True)

        for d in self._lire_json(FICHIER_UTILISATEURS):
            u = Utilisateur.from_dict(d)
            self.utilisateurs[u.email] = u

        for d in self._lire_json(FICHIER_OBJETS):
            o = Objet.from_dict(d)
            self.objets[o.id] = o

        for d in self._lire_json(FICHIER_ENCHERES):
            e = Enchere.from_dict(d)
            self.encheres[e.id] = e
            if not e.est_cloturee:
                self.encheres_actives.append(e.id)

    def sauvegarder(self) -> None:
        """Sauvegarde toutes les données dans les fichiers JSON."""
        os.makedirs(DATA_DIR, exist_ok=True)
        self._ecrire_json(FICHIER_UTILISATEURS,
                          [u.to_dict() for u in self.utilisateurs.values()])
        self._ecrire_json(FICHIER_OBJETS,
                          [o.to_dict() for o in self.objets.values()])
        self._ecrire_json(FICHIER_ENCHERES,
                          [e.to_dict() for e in self.encheres.values()])

    # ── Gestion des utilisateurs ─────────────────────────────────────────────

    def inscrire(self, nom: str, email: str, mot_de_passe: str) -> Utilisateur | None:
        """Inscrit un nouvel utilisateur.

        Returns:
            Utilisateur créé, ou None si email déjà pris ou champ vide.
        """
        if not nom or not email or not mot_de_passe:
            return None
        if email in self.utilisateurs:
            return None
        u = Utilisateur.inscrire(nom, email, mot_de_passe)
        self.utilisateurs[u.email] = u
        self.sauvegarder()
        return u

    def connecter(self, email: str, mot_de_passe: str) -> Utilisateur | None:
        """Connecte un utilisateur existant.

        Returns:
            Utilisateur connecté, ou None si identifiants incorrects.
        """
        u = self.utilisateurs.get(email)
        if u and u.se_connecter(email, mot_de_passe):
            self.utilisateur_connecte = u
            return u
        return None

    def deconnecter(self) -> None:
        """Déconnecte l'utilisateur actif et sauvegarde."""
        self.sauvegarder()
        self.utilisateur_connecte = None

    # ── Gestion des objets ───────────────────────────────────────────────────

    def deposer_objet(
        self, titre: str, description: str, prix_depart: float, duree_tours: int = 1
    ) -> Objet | None:
        """Dépose un objet en vente pour l'utilisateur connecté.

        Returns:
            Objet créé, ou None si non connecté ou prix invalide.
        """
        if not self.utilisateur_connecte:
            return None
        if prix_depart <= 0:
            return None

        objet = Objet(titre, description, prix_depart,
                      self.utilisateur_connecte.email, duree_tours)
        objet.mettre_en_vente()
        self.objets[objet.id] = objet
        self.utilisateur_connecte.objets_en_vente.append(objet.id)

        date_fin = datetime.now().isoformat(timespec="seconds")
        enchere = Enchere(objet.id, prix_depart, date_fin)
        self.encheres[enchere.id] = enchere
        self.encheres_actives.append(enchere.id)

        self.sauvegarder()
        return objet

    def afficher_objets(self) -> None:
        """Affiche tous les objets actifs en vente (méthode CLI)."""
        actifs = [o for o in self.objets.values() if o.est_disponible()]
        if not actifs:
            print("Aucun objet en vente pour le moment.")
            return
        for o in actifs:
            print(o)

    # ── Gestion des enchères ─────────────────────────────────────────────────

    def placer_mise(self, id_enchere: int, montant: float) -> bool:
        """Place une mise pour l'utilisateur connecté.

        Vérifie : connexion, enchère active, vendeur ≠ enchérisseur, solde suffisant.

        Returns:
            True si la mise est acceptée, False sinon.
        """
        if not self.utilisateur_connecte:
            return False

        enchere = self.encheres.get(id_enchere)
        if not enchere or enchere.est_cloturee:
            return False

        objet = self.objets.get(enchere.id_objet)
        if not objet:
            return False

        # Restriction CDC : un vendeur ne peut pas miser sur son propre objet
        if objet.vendeur == self.utilisateur_connecte.email:
            return False

        if self.utilisateur_connecte.solde < montant:
            return False

        if enchere.placer_mise(self.utilisateur_connecte.email, montant):
            self.utilisateur_connecte.debiter(montant, f"Mise enchère #{id_enchere}")
            self.utilisateur_connecte.rejoindre_enchere(id_enchere)
            self.sauvegarder()
            return True
        return False

    def cloturer_enchere(self, id_enchere: int) -> dict | None:
        """Clôture une enchère et effectue les transactions financières.

        Returns:
            dict résultat de la clôture, ou None si introuvable/déjà clôturée.
        """
        enchere = self.encheres.get(id_enchere)
        if not enchere or enchere.est_cloturee:
            return None

        resultat = enchere.cloturer()
        objet = self.objets.get(enchere.id_objet)

        if resultat["vendu"]:
            objet.marquer_vendu()
            vendeur = self.utilisateurs.get(objet.vendeur)
            if vendeur:
                vendeur.crediter(resultat["montant_final"],
                                 f"Vente objet #{objet.id}")
        else:
            objet.marquer_non_vendu()

        if id_enchere in self.encheres_actives:
            self.encheres_actives.remove(id_enchere)

        self.sauvegarder()
        return resultat

    # ── Interface CLI (Bloc 6) ────────────────────────────────────────────────

    def lancer(self) -> None:
        """Point d'entrée CLI — implémenté dans main.py."""
        print("=== Plateforme d'Enchères en Ligne ===")
        print("Lancez main.py pour démarrer.")

    # ── Helpers internes ─────────────────────────────────────────────────────

    @staticmethod
    def _lire_json(chemin: str) -> list:
        """Lit un fichier JSON. Crée le fichier vide si absent."""
        if not os.path.exists(chemin):
            Plateforme._ecrire_json(chemin, [])
            return []
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"[ERREUR] Fichier corrompu : {chemin}. Arrêt du programme.")
            raise SystemExit(1)

    @staticmethod
    def _ecrire_json(chemin: str, donnees) -> None:
        """Écrit des données dans un fichier JSON."""
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2)

    def get_tableau_de_bord(self) -> dict:
        """Retourne un résumé de l'état de la plateforme."""
        return {
            "nb_utilisateurs": len(self.utilisateurs),
            "nb_objets": len(self.objets),
            "nb_encheres_actives": len(self.encheres_actives),
            "categories": self.categories,
        }
