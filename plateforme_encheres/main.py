"""
main.py
Point d'entrée de la Plateforme d'Enchères en Ligne.

Bloc 6 — Interface CLI complète.
Inspiré du travail de ASSOCLE Pacifique, corrigé et intégré.
"""

from models.plateforme import Plateforme


def afficher_menu_accueil():
    print("\n===== PLATEFORME D'ENCHERES =====")
    print("1. S'inscrire")
    print("2. Se connecter")
    print("0. Quitter")
    print("=================================")


def afficher_menu_connecte(nom):
    print(f"\n===== BIENVENUE {nom.upper()} =====")
    print("1. Voir les objets en vente")
    print("2. Mettre un objet en vente")
    print("3. Faire une mise")
    print("4. Clôturer une enchère")
    print("5. Mon solde et historique")
    print("6. Se déconnecter")
    print("0. Quitter")
    print("==================================")


def saisir_float(invite: str) -> float | None:
    """Demande un nombre décimal. Retourne None si la saisie est invalide."""
    try:
        return float(input(invite))
    except ValueError:
        print("  ✗ Veuillez entrer un nombre valide.")
        return None


def main():
    plateforme = Plateforme()

    while True:
        if not plateforme.utilisateur_connecte:
            afficher_menu_accueil()
            choix = input("Votre choix : ").strip()

            # ── Inscription ──────────────────────────────────────────────
            if choix == "1":
                nom = input("Nom d'utilisateur : ").strip()
                email = input("Email : ").strip()
                mdp = input("Mot de passe : ").strip()

                if not nom or not email or not mdp:
                    print("  ✗ Tous les champs sont obligatoires.")
                    continue

                u = plateforme.inscrire(nom, email, mdp)
                if u:
                    print(f"  ✓ Compte créé ! Bienvenue {nom}. Solde initial : {u.solde} FCFA.")
                else:
                    print("  ✗ Cet email est déjà utilisé.")

            # ── Connexion ────────────────────────────────────────────────
            elif choix == "2":
                email = input("Email : ").strip()
                mdp = input("Mot de passe : ").strip()

                u = plateforme.connecter(email, mdp)
                if u:
                    print(f"  ✓ Connexion réussie. Bonjour {u.nom} !")
                else:
                    print("  ✗ Email ou mot de passe incorrect.")

            elif choix == "0":
                print("Au revoir !")
                break

            else:
                print("  ✗ Choix invalide, réessayez.")

        else:
            u = plateforme.utilisateur_connecte
            afficher_menu_connecte(u.nom)
            choix = input("Votre choix : ").strip()

            # ── Voir les objets en vente ──────────────────────────────────
            if choix == "1":
                actifs = [
                    o for o in plateforme.objets.values()
                    if o.est_disponible()
                ]
                if not actifs:
                    print("  Aucun objet en vente pour le moment.")
                else:
                    print(f"\n  {'ID':<5} {'Titre':<20} {'Prix départ':>12} {'Offre actuelle':>15} {'Vendeur'}")
                    print("  " + "-" * 70)
                    for o in actifs:
                        enc = next(
                            (e for e in plateforme.encheres.values()
                             if e.id_objet == o.id and not e.est_cloturee),
                            None
                        )
                        offre = f"{enc.montant_actuel} FCFA" if enc else "-"
                        print(f"  {o.id:<5} {o.titre:<20} {o.prix_depart:>10} F {offre:>15}   {o.vendeur}")

            # ── Mettre en vente ──────────────────────────────────────────
            elif choix == "2":
                titre = input("Titre de l'objet : ").strip()
                description = input("Description : ").strip()
                if not titre or not description:
                    print("  ✗ Titre et description sont obligatoires.")
                    continue
                prix = saisir_float("Prix de départ (FCFA) : ")
                if prix is None:
                    continue
                if prix <= 0:
                    print("  ✗ Le prix de départ doit être supérieur à zéro.")
                    continue
                duree = input("Durée (en tours, défaut=1) : ").strip()
                duree = int(duree) if duree.isdigit() else 1

                o = plateforme.deposer_objet(titre, description, prix, duree)
                if o:
                    print(f"  ✓ Objet '{titre}' mis en vente à {prix} FCFA.")

            # ── Faire une mise ───────────────────────────────────────────
            elif choix == "3":
                id_enc = input("ID de l'enchère : ").strip()
                if not id_enc.isdigit():
                    print("  ✗ ID invalide.")
                    continue
                montant = saisir_float("Montant de la mise (FCFA) : ")
                if montant is None:
                    continue

                resultat = plateforme.placer_mise(int(id_enc), montant)
                if resultat:
                    print(f"  ✓ Mise de {montant} FCFA acceptée !")
                else:
                    enc = plateforme.encheres.get(int(id_enc))
                    obj = plateforme.objets.get(enc.id_objet) if enc else None
                    if not enc:
                        print("  ✗ Enchère introuvable.")
                    elif enc.est_cloturee:
                        print("  ✗ Cette enchère est déjà clôturée.")
                    elif obj and obj.vendeur == u.email:
                        print("  ✗ Vous ne pouvez pas enchérir sur votre propre objet.")
                    elif u.solde < montant:
                        print(f"  ✗ Solde insuffisant. Votre solde : {u.solde} FCFA.")
                    else:
                        print(f"  ✗ La mise doit être supérieure à {enc.montant_actuel} FCFA.")

            # ── Clôturer une enchère ─────────────────────────────────────
            elif choix == "4":
                id_enc = input("ID de l'enchère à clôturer : ").strip()
                if not id_enc.isdigit():
                    print("  ✗ ID invalide.")
                    continue

                resultat = plateforme.cloturer_enchere(int(id_enc))
                if not resultat:
                    print("  ✗ Enchère introuvable ou déjà clôturée.")
                elif resultat["vendu"]:
                    print(f"  ✓ Enchère clôturée. Gagnant : {resultat['gagnant']} "
                          f"avec {resultat['montant_final']} FCFA.")
                else:
                    print("  ✓ Enchère clôturée. Aucune offre — objet non vendu.")

            # ── Solde et historique ──────────────────────────────────────
            elif choix == "5":
                print(f"\n  Solde actuel : {u.solde} FCFA")
                if not u.historique:
                    print("  Aucune transaction.")
                else:
                    print(f"\n  {'Type':<8} {'Montant':>12}   Motif")
                    print("  " + "-" * 45)
                    for t in u.historique:
                        type_op = t[0].upper()
                        montant = t[1]
                        motif = t[2] if len(t) > 2 else ""
                        print(f"  {type_op:<8} {montant:>10} F   {motif}")

            # ── Déconnexion ──────────────────────────────────────────────
            elif choix == "6":
                plateforme.sauvegarder()
                plateforme.utilisateur_connecte = None
                print("  ✓ Déconnecté. À bientôt !")

            elif choix == "0":
                plateforme.sauvegarder()
                print("Au revoir !")
                break

            else:
                print("  ✗ Choix invalide, réessayez.")


if __name__ == "__main__":
    main()
