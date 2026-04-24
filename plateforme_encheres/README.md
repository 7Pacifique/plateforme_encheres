# Plateforme d'Enchères en Ligne 🏷️

**Projet 5** — Cours de Programmation Python, Licence 2  
Université de Parakou | Année 2025-2026

**Étudiants :** GBESSO Segnon Amour Ozias & ASSOCLE Pacifique  
**Enseignant :** Dr MOUSSE Mikael

---

## Description

Simulation d'une plateforme de vente aux enchères en ligne. Les utilisateurs disposent
d'un compte virtuel (10 000 FCFA) et peuvent déposer des objets en vente et enchérir.

---

## Structure du projet

```
plateforme_encheres/
├── main.py                  # Point d'entrée (Bloc 6)
├── models/
│   ├── __init__.py
│   ├── utilisateur.py       # Classe Utilisateur (Bloc 3)
│   ├── objet.py             # Classe Objet (Bloc 3)
│   ├── enchere.py           # Classe Enchere (Bloc 3)
│   └── plateforme.py        # Classe Plateforme (Bloc 3)
├── data/
│   ├── utilisateurs.json    # Sauvegarde des comptes (Bloc 4)
│   ├── objets.json          # Sauvegarde des objets (Bloc 4)
│   └── encheres.json        # Sauvegarde des enchères (Bloc 4)
├── tests/
│   └── test_enchere.py      # Tests unitaires (Bloc 5)
├── types_complexes.py       # Démonstration types de données (Bloc 2)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

```bash
# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer la démonstration des types de données
python types_complexes.py
```

---

## Blocs du projet

| Bloc | Thème                     | Statut        |
|------|---------------------------|---------------|
| 1    | Cahier des charges        | Livré       |
| 2    | Workflow & Fondations     | Livré       |
| 3    | Architecture POO          | Livré    |
| 4    | Persistance JSON          | Livré    |
| 5    | Qualité (Tests)           | À faire    |
| 6    | Interface CLI & Livraison | À faire    |