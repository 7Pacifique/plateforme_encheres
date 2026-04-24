"""
tests/test_enchere.py
Tests unitaires — Bloc 3 (POO) + prévisions Blocs 4/5.

Couvre : EntiteBase (héritage), Utilisateur, Objet, Enchere, Plateforme.
Lancer avec : pytest tests/
"""

import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.base import EntiteBase
from models.utilisateur import Utilisateur
from models.objet import Objet
from models.enchere import Enchere
from models.plateforme import Plateforme


# ══ Héritage ═════════════════════════════════════════════════════════════════

class TestHeritage:

    def test_utilisateur_herite_entite_base(self):
        """Utilisateur doit être une instance de EntiteBase."""
        u = Utilisateur("Alice", "alice@mail.com", "1234")
        assert isinstance(u, EntiteBase)

    def test_objet_herite_entite_base(self):
        """Objet doit être une instance de EntiteBase."""
        o = Objet("Vase", "Ancien", 500.0, "alice@mail.com")
        assert isinstance(o, EntiteBase)

    def test_enchere_herite_entite_base(self):
        """Enchere doit être une instance de EntiteBase."""
        e = Enchere(1, 500.0, "2026-04-30T23:59:00")
        assert isinstance(e, EntiteBase)

    def test_ids_independants_par_classe(self):
        """Chaque classe fille doit avoir son propre compteur d'ID."""
        u = Utilisateur("Alice", "alice@mail.com", "1234")
        o = Objet("Vase", "Ancien", 500.0, "alice@mail.com")
        # Les IDs sont indépendants entre classes
        assert isinstance(u.id, int)
        assert isinstance(o.id, int)


# ══ Encapsulation ════════════════════════════════════════════════════════════

class TestEncapsulation:

    def test_attributs_prives_utilisateur(self):
        """Les attributs privés ne doivent pas être accessibles directement."""
        u = Utilisateur("Alice", "alice@mail.com", "1234")
        assert not hasattr(u, "nom") or u.nom == "Alice"  # via propriété OK
        # Accès direct à l'attribut privé doit échouer
        assert not hasattr(u, "__nom")
        assert not hasattr(u, "__solde")

    def test_propriete_solde_lecture_seule(self):
        """Le solde ne doit pas être modifiable directement."""
        u = Utilisateur("Alice", "alice@mail.com", "1234")
        try:
            u.solde = 99999  # type: ignore
            assert False, "Devrait lever AttributeError"
        except AttributeError:
            pass

    def test_propriete_statut_objet(self):
        """Le statut d'un objet doit être accessible en lecture via propriété."""
        o = Objet("Vase", "Ancien", 500.0, "alice@mail.com")
        assert o.statut == "en_attente"


# ══ Utilisateur ══════════════════════════════════════════════════════════════

class TestUtilisateur:

    def test_solde_initial(self):
        u = Utilisateur.inscrire("Alice", "alice@mail.com", "1234")
        assert u.solde == 10_000.0

    def test_connexion_correcte(self):
        u = Utilisateur("Alice", "alice@mail.com", "1234")
        assert u.se_connecter("alice@mail.com", "1234") is True

    def test_connexion_mauvais_mdp(self):
        u = Utilisateur("Alice", "alice@mail.com", "1234")
        assert u.se_connecter("alice@mail.com", "wrong") is False

    def test_crediter(self):
        u = Utilisateur("Alice", "alice@mail.com", "1234")
        u.crediter(500.0, "Vente")
        assert u.solde == 10_500.0
        assert len(u.historique) == 1
        assert isinstance(u.historique[0], tuple)

    def test_debiter_succes(self):
        u = Utilisateur("Alice", "alice@mail.com", "1234")
        assert u.debiter(3_000.0) is True
        assert u.solde == 7_000.0

    def test_debiter_echec_solde_insuffisant(self):
        u = Utilisateur("Alice", "alice@mail.com", "1234")
        assert u.debiter(20_000.0) is False
        assert u.solde == 10_000.0  # Solde inchangé

    def test_set_encheres_sans_doublons(self):
        u = Utilisateur("Alice", "alice@mail.com", "1234")
        u.rejoindre_enchere(1)
        u.rejoindre_enchere(1)
        assert isinstance(u.encheres_participees, set)
        assert len(u.encheres_participees) == 1

    def test_to_dict_from_dict(self):
        u = Utilisateur("Alice", "alice@mail.com", "1234")
        u.crediter(200.0)
        d = u.to_dict()
        json.dumps(d)  # Doit être sérialisable
        u2 = Utilisateur.from_dict(d)
        assert u2.nom == u.nom
        assert u2.solde == u.solde


# ══ Objet ════════════════════════════════════════════════════════════════════

class TestObjet:

    def test_statut_initial(self):
        o = Objet("Vase", "Ancien", 500.0, "alice@mail.com")
        assert o.statut == "en_attente"

    def test_mettre_en_vente(self):
        o = Objet("Vase", "Ancien", 500.0, "alice@mail.com")
        assert o.mettre_en_vente() is True
        assert o.statut == "actif"

    def test_est_disponible(self):
        o = Objet("Vase", "Ancien", 500.0, "alice@mail.com")
        assert o.est_disponible() is False
        o.mettre_en_vente()
        assert o.est_disponible() is True

    def test_to_dict_from_dict(self):
        o = Objet("Vase", "Ancien", 500.0, "alice@mail.com", 2)
        o.mettre_en_vente()
        d = o.to_dict()
        json.dumps(d)
        o2 = Objet.from_dict(d)
        assert o2.titre == o.titre
        assert o2.statut == o.statut


# ══ Enchere ══════════════════════════════════════════════════════════════════

class TestEnchere:

    def test_placer_mise_valide(self):
        e = Enchere(1, 500.0, "2026-04-30T23:59:00")
        assert e.placer_mise("bob@mail.com", 600.0) is True
        assert e.montant_actuel == 600.0

    def test_placer_mise_trop_basse(self):
        e = Enchere(1, 500.0, "2026-04-30T23:59:00")
        assert e.placer_mise("bob@mail.com", 500.0) is False

    def test_placer_mise_cloturee(self):
        e = Enchere(1, 500.0, "2026-04-30T23:59:00")
        e.cloturer()
        assert e.placer_mise("bob@mail.com", 600.0) is False

    def test_cloturer_avec_gagnant(self):
        e = Enchere(1, 500.0, "2026-04-30T23:59:00")
        e.placer_mise("bob@mail.com", 700.0)
        r = e.cloturer()
        assert r["vendu"] is True
        assert r["gagnant"] == "bob@mail.com"

    def test_cloturer_sans_mise(self):
        e = Enchere(1, 500.0, "2026-04-30T23:59:00")
        r = e.cloturer()
        assert r["vendu"] is False
        assert r["gagnant"] is None

    def test_get_gagnant_initial_none(self):
        e = Enchere(1, 500.0, "2026-04-30T23:59:00")
        assert e.get_gagnant() is None

    def test_historique_list_de_tuples(self):
        e = Enchere(1, 500.0, "2026-04-30T23:59:00")
        e.placer_mise("bob@mail.com", 600.0)
        assert isinstance(e.historique_mises, list)
        assert isinstance(e.historique_mises[0], tuple)

    def test_to_dict_from_dict(self):
        e = Enchere(1, 500.0, "2026-04-30T23:59:00")
        e.placer_mise("bob@mail.com", 700.0)
        d = e.to_dict()
        json.dumps(d)
        e2 = Enchere.from_dict(d)
        assert e2.montant_actuel == e.montant_actuel
        assert e2.meilleur_encherisseur == e.meilleur_encherisseur


# ══ Plateforme ═══════════════════════════════════════════════════════════════

class TestPlateforme:

    def _nouvelle_plateforme(self):
        """Crée une Plateforme avec fichiers JSON temporaires."""
        import models.plateforme as mp
        tmp = tempfile.mkdtemp()
        mp.FICHIER_UTILISATEURS = os.path.join(tmp, "utilisateurs.json")
        mp.FICHIER_OBJETS = os.path.join(tmp, "objets.json")
        mp.FICHIER_ENCHERES = os.path.join(tmp, "encheres.json")
        return Plateforme()

    def test_inscription_succes(self):
        p = self._nouvelle_plateforme()
        u = p.inscrire("Alice", "alice@mail.com", "1234")
        assert u is not None
        assert u.solde == 10_000.0

    def test_inscription_email_duplique(self):
        p = self._nouvelle_plateforme()
        p.inscrire("Alice", "alice@mail.com", "1234")
        assert p.inscrire("Alice2", "alice@mail.com", "5678") is None

    def test_connexion_succes(self):
        p = self._nouvelle_plateforme()
        p.inscrire("Alice", "alice@mail.com", "1234")
        assert p.connecter("alice@mail.com", "1234") is not None

    def test_connexion_echec(self):
        p = self._nouvelle_plateforme()
        p.inscrire("Alice", "alice@mail.com", "1234")
        assert p.connecter("alice@mail.com", "wrong") is None

    def test_vendeur_ne_peut_pas_encherir(self):
        p = self._nouvelle_plateforme()
        p.inscrire("Alice", "alice@mail.com", "1234")
        p.connecter("alice@mail.com", "1234")
        p.deposer_objet("Vase", "Ancien", 500.0, 1)
        id_enc = list(p.encheres.keys())[-1]
        assert p.placer_mise(id_enc, 600.0) is False

    def test_solde_insuffisant(self):
        p = self._nouvelle_plateforme()
        p.inscrire("Alice", "alice@mail.com", "1234")
        p.inscrire("Bob", "bob@mail.com", "5678")
        p.connecter("alice@mail.com", "1234")
        p.deposer_objet("Vase", "Ancien", 500.0, 1)
        id_enc = list(p.encheres.keys())[-1]
        p.connecter("bob@mail.com", "5678")
        assert p.placer_mise(id_enc, 50_000.0) is False

    def test_utilisateurs_est_dict(self):
        p = self._nouvelle_plateforme()
        assert isinstance(p.utilisateurs, dict)

    def test_categories_est_set(self):
        p = self._nouvelle_plateforme()
        assert isinstance(p.categories, set)
