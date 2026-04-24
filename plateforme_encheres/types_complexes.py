"""
types_complexes.py
Démonstration des types de données complexes Python.

Bloc 2 — Fondations : illustration des types utilisés dans la Plateforme d'Enchères.
"""

# ══════════════════════════════════════════════════════════════════════════════
# 1. LIST — collection ordonnée et modifiable
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 55)
print("1. LIST — collection ordonnée et modifiable")
print("=" * 55)

# Dans notre projet : liste des enchères actives
encheres_actives = [1, 2, 3]
print(f"Enchères actives      : {encheres_actives}")

encheres_actives.append(4)          # Ajouter une enchère
print(f"Après append(4)       : {encheres_actives}")

encheres_actives.remove(2)          # Supprimer une enchère clôturée
print(f"Après remove(2)       : {encheres_actives}")

print(f"Première enchère      : {encheres_actives[0]}")
print(f"Nombre d'enchères     : {len(encheres_actives)}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. DICT — collection clé → valeur
# ══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 55)
print("2. DICT — collection clé → valeur")
print("=" * 55)

# Dans notre projet : profil d'un utilisateur
utilisateur = {
    "nom": "Alice",
    "email": "alice@mail.com",
    "solde": 10_000.0,
    "objets_en_vente": [3, 7],
}
print(f"Profil utilisateur    : {utilisateur}")
print(f"Nom                   : {utilisateur['nom']}")
print(f"Solde initial         : {utilisateur['solde']} FCFA")

utilisateur["solde"] -= 1_500.0     # Débit après une mise
print(f"Solde après débit     : {utilisateur['solde']} FCFA")

print(f"'email' dans dict     : {'email' in utilisateur}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. TUPLE — collection ordonnée et IMMUABLE
# ══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 55)
print("3. TUPLE — collection immuable")
print("=" * 55)

# Dans notre projet : enregistrement d'une transaction (ne change jamais)
transaction = ("debit", 1_500.0, "Mise enchère #3")
print(f"Transaction           : {transaction}")

type_op, montant, motif = transaction   # Dépaquetage
print(f"Dépaquetage           : type={type_op}, montant={montant}, motif={motif}")

# Tentative de modification → erreur attendue
try:
    transaction[1] = 9999  # type: ignore
except TypeError as e:
    print(f"Modification refusée  : {e}")

# Historique = liste de tuples
historique = [
    ("credit", 10_000.0, "Solde initial"),
    ("debit",   1_500.0, "Mise enchère #3"),
    ("credit",  2_000.0, "Vente objet #1"),
]
print(f"Historique            : {historique}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. SET — collection non ordonnée SANS DOUBLONS
# ══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 55)
print("4. SET — collection sans doublons")
print("=" * 55)

# Dans notre projet : enchérisseurs uniques sur un objet
encherisseurs = {"alice@mail.com", "bob@mail.com", "charlie@mail.com"}
print(f"Enchérisseurs         : {encherisseurs}")

encherisseurs.add("bob@mail.com")   # Doublon → ignoré automatiquement
print(f"Après add doublon     : {encherisseurs}  (toujours 3 éléments)")

encherisseurs.add("diana@mail.com")
print(f"Après add nouveau     : {encherisseurs}")

print(f"'bob' est présent     : {'bob@mail.com' in encherisseurs}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. RÉCAPITULATIF
# ══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 55)
print("5. RÉCAPITULATIF — Quel type pour quel usage ?")
print("=" * 55)

recap = {
    "list" : "Enchères actives, historique ordonné des mises",
    "dict" : "Profil utilisateur, données JSON, résultat de clôture",
    "tuple": "Transaction immuable, métadonnées fixes d'un objet",
    "set"  : "Enchérisseurs uniques, catégories sans doublons",
}
for type_py, usage in recap.items():
    print(f"  {type_py:<6} → {usage}")

print()
print("Fin de la démonstration.")
