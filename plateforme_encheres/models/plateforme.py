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
    def inscrire(self, nom, email, mot_de_passe):
        if email in self.utilisateurs:
            print("Cet email est déjà utilisé.")
            return False
        if not nom or not email or not mot_de_passe:
            print("Tous les champs sont obligatoires.")
            return False
        self.utilisateurs[email] = Utilisateur(nom, email, mot_de_passe)
        print(f"Compte créé avec succès. Bienvenue {nom} !")
        return True

    def connecter(self, email, mot_de_passe):
        if email not in self.utilisateurs:
            print("Email introuvable.")
            return False
        if self.utilisateurs[email].mot_de_passe != mot_de_passe:
            print("Mot de passe incorrect.")
            return False
        self.utilisateur_connecte = self.utilisateurs[email]
        print(f"Connexion réussie. Bonjour {self.utilisateur_connecte.nom} !")
        return True

    def deconnecter(self):
        self.utilisateur_connecte = None
        print("Vous êtes déconnecté.")    
