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
    self.charger()

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
    
    def cloturer_enchere(self, titre_objet):
        objet = self._trouver_objet(titre_objet)
        if not objet:
            print("Objet introuvable.")
            return False
        if objet.statut == "cloture":
            print("Cette enchère est déjà clôturée.")
            return False
        objet.cloturer()
        if objet.meilleur_encherisseur:
            vendeur = self.utilisateurs[objet.vendeur_email]
            vendeur.crediter(objet.meilleure_offre)
            print(f"Enchère clôturée. Gagnant : {objet.meilleur_encherisseur} avec {objet.meilleure_offre} FCFA.")
        else:
            print("Enchère clôturée. Aucune offre reçue, objet non vendu.")
        return True

    def afficher_objets(self):
        if not self.objets:
            print("Aucun objet en vente pour le moment.")
            return
        for objet in self.objets:
            print(objet)

    def sauvegarder(self):
        with open("data/utilisateurs.json", "w") as f:
            json.dump({email: u.to_dict() for email, u in self.utilisateurs.items()}, f, indent=4)
        with open("data/objets.json", "w") as f:
            json.dump([o.to_dict() for o in self.objets], f, indent=4)
        with open("data/encheres.json", "w") as f:
            json.dump([e.to_dict() for e in self.encheres], f, indent=4)
        print("Données sauvegardées.")


    def charger(self):
        if os.path.exists("data/utilisateurs.json"):
            with open("data/utilisateurs.json", "r") as f:
                try:
                    data = json.load(f)
                    for email, u in data.items():
                        utilisateur = Utilisateur(u["nom"], u["email"], u["mot_de_passe"])
                        utilisateur.solde = u["solde"]
                        utilisateur.historique = u["historique"]
                        self.utilisateurs[email] = utilisateur
                except:
                    print("Erreur lors du chargement des utilisateurs.")

        if os.path.exists("data/objets.json"):
            with open("data/objets.json", "r") as f:
                try:
                    data = json.load(f)
                    for o in data:
                        objet = Objet(o["titre"], o["description"], o["prix_depart"], o["vendeur_email"])
                        objet.meilleure_offre = o["meilleure_offre"]
                        objet.meilleur_encherisseur = o["meilleur_encherisseur"]
                        objet.statut = o["statut"]
                        objet.encherisseurs = set(o["encherisseurs"])
                        self.objets.append(objet)
                except:
                    print("Erreur lors du chargement des objets.")    