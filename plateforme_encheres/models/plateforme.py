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

    def mettre_en_vente(self, titre, description, prix_depart):
        if not self.utilisateur_connecte:
            print("Vous devez être connecté pour vendre un objet.")
            return False
        if prix_depart <= 0:
            print("Le prix de départ doit être supérieur à zéro.")
            return False
        objet = Objet(titre, description, prix_depart, self.utilisateur_connecte.email)
        self.objets.append(objet)
        print(f"Objet '{titre}' mis en vente à {prix_depart} FCFA.")
        return True

    def faire_une_mise(self, titre_objet, montant):
        if not self.utilisateur_connecte:
            print("Vous devez être connecté pour enchérir.")
            return False
        objet = self._trouver_objet(titre_objet)
        if not objet:
            print("Objet introuvable.")
            return False
        if objet.vendeur_email == self.utilisateur_connecte.email:
            print("Vous ne pouvez pas enchérir sur votre propre objet.")
            return False
        if not self.utilisateur_connecte.debiter(montant):
            print("Solde insuffisant.")
            return False
        if not objet.recevoir_mise(montant, self.utilisateur_connecte.email):
            print(f"La mise doit être supérieure à {objet.meilleure_offre} FCFA.")
            self.utilisateur_connecte.crediter(montant)
            return False
        enchere = Enchere(titre_objet, self.utilisateur_connecte.email, montant)
        self.encheres.append(enchere)
        print(f"Mise de {montant} FCFA acceptée sur '{titre_objet}'.")
        return True

    def _trouver_objet(self, titre):
        for objet in self.objets:
            if objet.titre == titre:
                return objet
        return None    