"""
models/enchere.py
Classe Enchere — à implémenter au Bloc 3.

Attributs prévus : objet, montant_actuel, meilleur_encherisseur, date_fin
Méthodes prévues : placer_mise(), cloturer(), get_gagnant(), to_dict(), from_dict()
"""

# TODO Bloc 3 : implémenter la classe Enchere


from datetime import datetime

class Enchere:

    def __init__(self, objet_titre, encherisseur_email, montant):
        self.objet_titre = objet_titre
        self.encherisseur_email = encherisseur_email
        self.montant = montant
        self.date_heure = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def to_dict(self):
        return {
            "objet_titre": self.objet_titre,
            "encherisseur_email": self.encherisseur_email,
            "montant": self.montant,
            "date_heure": self.date_heure
        }

    def __str__(self):
        return f"{self.encherisseur_email} a mise {self.montant} FCFA sur {self.objet_titre} le {self.date_heure}"    