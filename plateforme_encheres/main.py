"""
main.py
Point d'entrée de la Plateforme d'Enchères en Ligne.

Bloc 6 — Interface CLI
"""

from models.plateforme import Plateforme
from models.exceptions import (
    EmailDejaUtiliseError, IdentifiantsInvalidesError, ChampVideError,
    PrixInvalideError, SoldeInsuffisantError, VendeurEncheritError,
    MiseTropBasseError, EnchereIntrouvableError, EnchereClotureeError,
    PlateForme_Erreur,
)


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

    try:
        while True:
            if not plateforme.utilisateur_connecte:
                afficher_menu_accueil()
                choix = input("Votre choix : ").strip()

                # ── Inscription ──────────────────────────────────────────
                if choix == "1":
                    nom   = input("Nom d'utilisateur : ").strip()
                    email = input("Email : ").strip()
                    mdp   = input("Mot de passe : ").strip()
                    try:
                        u = plateforme.inscrire(nom, email, mdp)
                        print(f"  ✓ Compte créé ! Bienvenue {nom}."
                              f" Solde initial : {u.solde} FCFA.")
                    except ChampVideError as e:
                        print(f"  ✗ {e}")
                    except EmailDejaUtiliseError as e:
                        print(f"  ✗ {e}")

                # ── Connexion ────────────────────────────────────────────
                elif choix == "2":
                    email = input("Email : ").strip()
                    mdp   = input("Mot de passe : ").strip()
                    try:
                        u = plateforme.connecter(email, mdp)
                        print(f"  ✓ Connexion réussie. Bonjour {u.nom} !")
                    except IdentifiantsInvalidesError as e:
                        print(f"  ✗ {e}")

                elif choix == "0":
                    print("Au revoir !")
                    break

                else:
                    print("  ✗ Choix invalide, réessayez.")

            else:
                u = plateforme.utilisateur_connecte
                afficher_menu_connecte(u.nom)
                choix = input("Votre choix : ").strip()

                # ── Voir les objets en vente ──────────────────────────────
                if choix == "1":
                    actifs = [o for o in plateforme.objets.values()
                              if o.est_disponible()]
                    if not actifs:
                        print("  Aucun objet en vente pour le moment.")
                    else:
                        print(f"\n  {'ID enc.':<8} {'Titre':<20} {'Prix départ':>12}"
                              f" {'Offre actuelle':>15}   Vendeur")
                        print("  " + "-" * 72)
                        for o in actifs:
                            enc = next(
                                (e for e in plateforme.encheres.values()
                                 if e.id_objet == o.id and not e.est_cloturee),
                                None
                            )
                            id_enc = str(enc.id) if enc else "-"
                            offre  = f"{enc.montant_actuel} F" if enc else "-"
                            print(f"  {id_enc:<8} {o.titre:<20}"
                                  f" {o.prix_depart:>10} F"
                                  f" {offre:>15}   {o.vendeur}")

                # ── Mettre en vente ──────────────────────────────────────
                elif choix == "2":
                    titre       = input("Titre de l'objet : ").strip()
                    description = input("Description : ").strip()
                    prix = saisir_float("Prix de départ (FCFA) : ")
                    if prix is None:
                        continue
                    duree = input("Durée (en tours, défaut=1) : ").strip()
                    duree = int(duree) if duree.isdigit() and int(duree) > 0 else 1
                    try:
                        o = plateforme.deposer_objet(titre, description, prix, duree)
                        print(f"  ✓ '{o.titre}' mis en vente à {prix} FCFA.")
                    except ChampVideError as e:
                        print(f"  ✗ {e}")
                    except PrixInvalideError as e:
                        print(f"  ✗ {e}")

                # ── Faire une mise ───────────────────────────────────────
                elif choix == "3":
                    id_enc = input("ID de l'enchère (voir colonne 'ID enc.') : ").strip()
                    if not id_enc.isdigit():
                        print("  ✗ ID invalide.")
                        continue
                    montant = saisir_float("Montant de la mise (FCFA) : ")
                    if montant is None:
                        continue
                    try:
                        plateforme.placer_mise(int(id_enc), montant)
                        print(f"  ✓ Mise de {montant} FCFA acceptée !")
                    except EnchereIntrouvableError as e:
                        print(f"  ✗ {e}")
                    except EnchereClotureeError as e:
                        print(f"  ✗ {e}")
                    except VendeurEncheritError as e:
                        print(f"  ✗ {e}")
                    except SoldeInsuffisantError as e:
                        print(f"  ✗ {e}  Votre solde : {u.solde} FCFA.")
                    except MiseTropBasseError as e:
                        print(f"  ✗ {e}")

                # ── Clôturer une enchère ─────────────────────────────────
                elif choix == "4":
                    id_enc = input("ID de l'enchère à clôturer : ").strip()
                    if not id_enc.isdigit():
                        print("  ✗ ID invalide.")
                        continue
                    try:
                        resultat = plateforme.cloturer_enchere(int(id_enc))
                        if resultat["vendu"]:
                            print(f"  ✓ Gagnant : {resultat['gagnant']}"
                                  f" — {resultat['montant_final']} FCFA.")
                        else:
                            print("  ✓ Enchère clôturée — aucune offre, objet non vendu.")
                    except EnchereIntrouvableError as e:
                        print(f"  ✗ {e}")
                    except EnchereClotureeError as e:
                        print(f"  ✗ {e}")

                # ── Solde et historique ──────────────────────────────────
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
                            motif   = t[2] if len(t) > 2 else ""
                            print(f"  {type_op:<8} {montant:>10} F   {motif}")

                # ── Déconnexion ──────────────────────────────────────────
                elif choix == "6":
                    plateforme.deconnecter()
                    print("  ✓ Déconnecté. À bientôt !")

                elif choix == "0":
                    plateforme.sauvegarder()
                    print("Au revoir !")
                    break

                else:
                    print("  ✗ Choix invalide, réessayez.")

    except KeyboardInterrupt:
        # Ctrl+C — sauvegarde propre avant de quitter
        print("\n\n  Interruption détectée. Sauvegarde en cours...")
        plateforme.sauvegarder()
        print("  Données sauvegardées. Au revoir !")


if __name__ == "__main__":
    main()
