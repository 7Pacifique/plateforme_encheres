"""
models/utilisateur.py
Classe Utilisateur — à implémenter au Bloc 3.

Attributs prévus : nom, email, mot_de_passe, solde, historique
Méthodes prévues : inscrire(), se_connecter(), crediter(), debiter(), to_dict(), from_dict()
"""

# TODO Bloc 3 : implémenter la classe Utilisateur


class Utilisateur:

    def __init__(self, nom, email, mot_de_passe):
        self.nom = nom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.solde = 10000
        self.historique = []
        self.encheres_en_cours = set()