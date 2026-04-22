"""
main.py
Point d'entrée de la Plateforme d'Enchères en Ligne.

À implémenter au Bloc 6.
"""

# TODO Bloc 6 : lancer l'interface CLI


from models.plateforme import Plateforme

def afficher_menu():
    print("\n===== PLATEFORME D'ENCHERES =====")
    print("1. S'inscrire")
    print("2. Se connecter")
    print("3. Se déconnecter")
    print("4. Mettre un objet en vente")
    print("5. Voir les objets en vente")
    print("6. Faire une mise")
    print("7. Clôturer une enchère")
    print("8. Sauvegarder")
    print("0. Quitter")
    print("=================================")

def main():
    plateforme = Plateforme()
    while True:
        afficher_menu()
        choix = input("Votre choix : ")

        if choix == "1":
            nom = input("Nom : ")
            email = input("Email : ")
            mdp = input("Mot de passe : ")
            plateforme.inscrire(nom, email, mdp)

        elif choix == "2":
            email = input("Email : ")
            mdp = input("Mot de passe : ")
            plateforme.connecter(email, mdp)

        elif choix == "3":
            plateforme.deconnecter()

        elif choix == "4":
            titre = input("Titre de l'objet : ")
            description = input("Description : ")
            prix = float(input("Prix de départ (FCFA) : "))
            plateforme.mettre_en_vente(titre, description, prix)

        elif choix == "5":
            plateforme.afficher_objets()

        elif choix == "6":
            titre = input("Titre de l'objet : ")
            montant = float(input("Montant de la mise (FCFA) : "))
            plateforme.faire_une_mise(titre, montant)

        elif choix == "7":
            titre = input("Titre de l'objet : ")
            plateforme.cloturer_enchere(titre)

        elif choix == "8":
            plateforme.sauvegarder()

        elif choix == "0":
            print("Au revoir !")
            break

        else:
            print("Choix invalide, réessayez.")

if __name__ == "__main__":
    main()