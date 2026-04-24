"""
tests/test_enchere.py
Tests unitaires — à implémenter au Bloc 5.

Couvrira : Utilisateur, Objet, Enchere, Plateforme.
Lancer avec : pytest tests/
"""

# TODO Bloc 5 : écrire les tests unitaires avec Pytest


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.utilisateur import Utilisateur
from models.objet import Objet
from models.enchere import Enchere


def test_creation_utilisateur():
    u = Utilisateur("Ozias", "ozias@mail.com", "1234")
    assert u.nom == "Ozias"
    assert u.solde == 10000


def test_debiter_solde_suffisant():
    u = Utilisateur("Ozias", "ozias@mail.com", "1234")
    resultat = u.debiter(3000)
    assert resultat == True
    assert u.solde == 7000


def test_debiter_solde_insuffisant():
    u = Utilisateur("Ozias", "ozias@mail.com", "1234")
    resultat = u.debiter(20000)
    assert resultat == False
    assert u.solde == 10000


def test_crediter():
    u = Utilisateur("Ozias", "ozias@mail.com", "1234")
    u.crediter(5000)
    assert u.solde == 15000


def test_mise_acceptee():
    o = Objet("Velo", "Velo rouge", 5000, "vendeur@mail.com")
    resultat = o.recevoir_mise(6000, "acheteur@mail.com")
    assert resultat == True
    assert o.meilleure_offre == 6000


def test_mise_trop_basse():
    o = Objet("Velo", "Velo rouge", 5000, "vendeur@mail.com")
    resultat = o.recevoir_mise(3000, "acheteur@mail.com")
    assert resultat == False


def test_mise_sur_enchere_cloturee():
    o = Objet("Velo", "Velo rouge", 5000, "vendeur@mail.com")
    o.cloturer()
    resultat = o.recevoir_mise(6000, "acheteur@mail.com")
    assert resultat == False