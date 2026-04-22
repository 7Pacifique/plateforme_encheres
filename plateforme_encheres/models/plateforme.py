"""
models/plateforme.py
Classe Plateforme — à implémenter au Bloc 3.

Attributs prévus : utilisateurs, objets, encheres
Méthodes prévues : charger_donnees(), sauvegarder(), lancer()
"""

# TODO Bloc 3 : implémenter la classe Plateforme


import json
import os
from models.utilisateur import Utilisateur
from models.objet import Objet
from models.enchere import Enchere

class Plateforme:

    def __init__(self):
        self.utilisateurs = {}
        self.objets = []
        self.encheres = []
        self.utilisateur_connecte = None
