"""
models/objet.py
Classe Objet — à implémenter au Bloc 3.

Attributs prévus : titre, description, prix_depart, vendeur, statut
Méthodes prévues : mettre_en_vente(), est_disponible(), to_dict(), from_dict()
"""

# TODO Bloc 3 : implémenter la classe Objet

class Objet:

    def __init__(self, titre, description, prix_depart, vendeur_email):
        self.titre = titre
        self.description = description
        self.prix_depart = prix_depart
        self.vendeur_email = vendeur_email
        self.meilleure_offre = prix_depart
        self.meilleur_encherisseur = None
        self.statut = "en_cours"
        self.encherisseurs = set()

    def recevoir_mise(self, montant, email_encherisseur):
        if self.statut == "cloture":
            return False
        if montant <= self.meilleure_offre:
            return False
        self.meilleure_offre = montant
        self.meilleur_encherisseur = email_encherisseur
        self.encherisseurs.add(email_encherisseur)
        return True

    def cloturer(self):
        self.statut = "cloture"

    def to_dict(self):
        return {
            "titre": self.titre,
            "description": self.description,
            "prix_depart": self.prix_depart,
            "vendeur_email": self.vendeur_email,
            "meilleure_offre": self.meilleure_offre,
            "meilleur_encherisseur": self.meilleur_encherisseur,
            "statut": self.statut,
            "encherisseurs": list(self.encherisseurs)
        }

    def __str__(self):
        return f"{self.titre} | Offre actuelle : {self.meilleure_offre} FCFA | Statut : {self.statut}"    