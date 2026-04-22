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