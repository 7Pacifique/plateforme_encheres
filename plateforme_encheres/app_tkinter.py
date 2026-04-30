"""
app_tkinter.py
Interface graphique de la Plateforme d'Enchères en Ligne.

Bloc 6 — GUI avec Tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from models.plateforme import Plateforme
from models.exceptions import (
    EmailDejaUtiliseError, IdentifiantsInvalidesError, ChampVideError,
    PrixInvalideError, SoldeInsuffisantError, VendeurEncheritError,
    MiseTropBasseError, EnchereIntrouvableError, EnchereClotureeError,
)

# ── Couleurs et polices ───────────────────────────────────────────────────────
COULEUR_FOND      = "#1e1e2e"
COULEUR_SURFACE   = "#2a2a3e"
COULEUR_ACCENT    = "#7c3aed"
COULEUR_ACCENT2   = "#10b981"
COULEUR_DANGER    = "#ef4444"
COULEUR_TEXTE     = "#e2e8f0"
COULEUR_SOUS_TEXT = "#94a3b8"
POLICE            = ("Segoe UI", 11)
POLICE_TITRE      = ("Segoe UI", 20, "bold")
POLICE_SOUS_TITRE = ("Segoe UI", 13, "bold")
POLICE_SMALL      = ("Segoe UI", 9)


def style_bouton(btn, couleur=COULEUR_ACCENT):
    btn.configure(
        bg=couleur, fg="white", font=("Segoe UI", 11, "bold"),
        relief="flat", padx=16, pady=8, cursor="hand2",
        activebackground=couleur, activeforeground="white",
    )


def style_champ(entry):
    entry.configure(
        bg=COULEUR_SURFACE, fg=COULEUR_TEXTE, font=POLICE,
        relief="flat", insertbackground=COULEUR_TEXTE,
        highlightthickness=1, highlightcolor=COULEUR_ACCENT,
        highlightbackground="#3a3a5e",
    )


def label(parent, text, police=POLICE, couleur=COULEUR_TEXTE, **kw):
    return tk.Label(parent, text=text, font=police, fg=couleur,
                    bg=COULEUR_FOND, **kw)


def label_surface(parent, text, police=POLICE, couleur=COULEUR_TEXTE, **kw):
    return tk.Label(parent, text=text, font=police, fg=couleur,
                    bg=COULEUR_SURFACE, **kw)


# ══════════════════════════════════════════════════════════════════════════════
# Fenêtre principale
# ══════════════════════════════════════════════════════════════════════════════

class App(tk.Tk):
    """Fenêtre principale — gère la navigation entre les écrans."""

    def __init__(self):
        super().__init__()
        self.plateforme = Plateforme()
        self.title("Plateforme d'Enchères en Ligne")
        self.geometry("900x620")
        self.configure(bg=COULEUR_FOND)
        self.resizable(False, False)

        # Conteneur unique — on swap les frames dedans
        self._conteneur = tk.Frame(self, bg=COULEUR_FOND)
        self._conteneur.pack(fill="both", expand=True)

        self._frame_actuelle = None
        self.afficher(EcranAccueil)

    def afficher(self, classe_frame, **kwargs):
        """Remplace l'écran actuel par un nouvel écran."""
        if self._frame_actuelle:
            self._frame_actuelle.destroy()
        self._frame_actuelle = classe_frame(self._conteneur, self, **kwargs)
        self._frame_actuelle.pack(fill="both", expand=True)

    def on_closing(self):
        self.plateforme.sauvegarder()
        self.destroy()


# ══════════════════════════════════════════════════════════════════════════════
# Écran d'accueil — Connexion / Inscription
# ══════════════════════════════════════════════════════════════════════════════

class EcranAccueil(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=COULEUR_FOND)
        self.app = app
        self._construire()

    def _construire(self):
        # Titre
        label(self, " Plateforme d'Enchères ", police=POLICE_TITRE).pack(pady=(50, 4))
        label(self, "Connectez-vous ou créez un compte pour commencer.",
              couleur=COULEUR_SOUS_TEXT).pack(pady=(0, 30))

        # Carte centrale
        carte = tk.Frame(self, bg=COULEUR_SURFACE, padx=40, pady=30)
        carte.pack(ipadx=10, ipady=10)

        # Onglets
        self._onglet = tk.StringVar(value="connexion")
        cadre_onglets = tk.Frame(carte, bg=COULEUR_SURFACE)
        cadre_onglets.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self._btn_connexion = tk.Button(
            cadre_onglets, text="Se connecter", font=("Segoe UI", 11, "bold"),
            relief="flat", padx=20, pady=6, cursor="hand2",
            command=lambda: self._basculer("connexion")
        )
        self._btn_inscription = tk.Button(
            cadre_onglets, text="S'inscrire", font=("Segoe UI", 11, "bold"),
            relief="flat", padx=20, pady=6, cursor="hand2",
            command=lambda: self._basculer("inscription")
        )
        self._btn_connexion.pack(side="left", padx=4)
        self._btn_inscription.pack(side="left", padx=4)

        # Champ nom (inscription seulement)
        self._ligne_nom = tk.Frame(carte, bg=COULEUR_SURFACE)
        self._ligne_nom.grid(row=1, column=0, columnspan=2, sticky="ew", pady=4)
        label_surface(self._ligne_nom, "Nom d'utilisateur").pack(anchor="w")
        self._champ_nom = tk.Entry(self._ligne_nom, width=32)
        style_champ(self._champ_nom)
        self._champ_nom.pack(fill="x", ipady=6)

        # Champ email
        label_surface(carte, "Email").grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))
        self._champ_email = tk.Entry(carte, width=32)
        style_champ(self._champ_email)
        self._champ_email.grid(row=3, column=0, columnspan=2, sticky="ew", ipady=6)

        # Champ mot de passe
        label_surface(carte, "Mot de passe").grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))
        self._champ_mdp = tk.Entry(carte, show="•", width=32)
        style_champ(self._champ_mdp)
        self._champ_mdp.grid(row=5, column=0, columnspan=2, sticky="ew", ipady=6)

        # Message d'erreur
        self._msg = tk.StringVar()
        tk.Label(carte, textvariable=self._msg, fg=COULEUR_DANGER,
                 bg=COULEUR_SURFACE, font=POLICE_SMALL).grid(
            row=6, column=0, columnspan=2, pady=(8, 0))

        # Bouton action
        self._btn_action = tk.Button(carte, command=self._soumettre)
        style_bouton(self._btn_action)
        self._btn_action.grid(row=7, column=0, columnspan=2, pady=(16, 0), sticky="ew")

        self._basculer("connexion")

    def _basculer(self, mode):
        self._onglet.set(mode)
        if mode == "connexion":
            self._btn_connexion.configure(bg=COULEUR_ACCENT, fg="white")
            self._btn_inscription.configure(bg="#3a3a5e", fg=COULEUR_SOUS_TEXT)
            self._ligne_nom.grid_remove()
            self._btn_action.configure(text="Se connecter")
        else:
            self._btn_inscription.configure(bg=COULEUR_ACCENT, fg="white")
            self._btn_connexion.configure(bg="#3a3a5e", fg=COULEUR_SOUS_TEXT)
            self._ligne_nom.grid()
            self._btn_action.configure(text="Créer mon compte")
        self._msg.set("")

    def _soumettre(self):
        email = self._champ_email.get().strip()
        mdp   = self._champ_mdp.get().strip()
        try:
            if self._onglet.get() == "connexion":
                self.app.plateforme.connecter(email, mdp)
                self.app.afficher(EcranPrincipal)
            else:
                nom = self._champ_nom.get().strip()
                self.app.plateforme.inscrire(nom, email, mdp)
                self.app.plateforme.connecter(email, mdp)
                self.app.afficher(EcranPrincipal)
        except (ChampVideError, EmailDejaUtiliseError,
                IdentifiantsInvalidesError) as e:
            self._msg.set(str(e))


# ══════════════════════════════════════════════════════════════════════════════
# Écran principal — tableau de bord
# ══════════════════════════════════════════════════════════════════════════════

class EcranPrincipal(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=COULEUR_FOND)
        self.app = app
        self._construire()

    def _construire(self):
        u = self.app.plateforme.utilisateur_connecte

        # ── Barre de navigation ──────────────────────────────────────────────
        nav = tk.Frame(self, bg=COULEUR_SURFACE, pady=10, padx=20)
        nav.pack(fill="x")

        label_surface(nav, " Enchères ", police=("Segoe UI", 14, "bold")).pack(side="left")

        # Solde
        self._var_solde = tk.StringVar(value=f"{u.solde:.0f} FCFA")
        tk.Label(nav, textvariable=self._var_solde, font=("Segoe UI", 11, "bold"),
                 fg=COULEUR_ACCENT2, bg=COULEUR_SURFACE).pack(side="left", padx=30)

        label_surface(nav, f"{u.nom}", couleur=COULEUR_SOUS_TEXT).pack(side="left")

        btn_deco = tk.Button(nav, text="Déconnexion", command=self._deconnecter,
                             font=POLICE_SMALL, relief="flat", padx=10, pady=4,
                             bg=COULEUR_DANGER, fg="white", cursor="hand2",
                             activebackground=COULEUR_DANGER)
        btn_deco.pack(side="right")

        # ── Corps principal ──────────────────────────────────────────────────
        corps = tk.Frame(self, bg=COULEUR_FOND)
        corps.pack(fill="both", expand=True, padx=20, pady=16)

        # Colonne gauche — Notebook avec onglets Actives / Historique
        col_gauche = tk.Frame(corps, bg=COULEUR_FOND)
        col_gauche.pack(side="left", fill="both", expand=True)

        self._notebook = ttk.Notebook(col_gauche)
        self._notebook.pack(fill="both", expand=True)

        # --- Onglet Enchères actives
        frame_actives = tk.Frame(self._notebook, bg=COULEUR_FOND)
        self._notebook.add(frame_actives, text="Enchères actives")

        entete = tk.Frame(frame_actives, bg=COULEUR_FOND)
        entete.pack(fill="x", pady=(0, 8))
        label(entete, "Enchères en cours", police=POLICE_SOUS_TITRE).pack(side="left")
        tk.Button(entete, text="↻ Rafraîchir", command=self._rafraichir,
                  font=POLICE_SMALL, relief="flat", padx=8, pady=3,
                  bg="#3a3a5e", fg=COULEUR_TEXTE, cursor="hand2").pack(side="right")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COULEUR_SURFACE,
                        foreground=COULEUR_TEXTE, fieldbackground=COULEUR_SURFACE,
                        rowheight=28, font=POLICE_SMALL)
        style.configure("Treeview.Heading", background="#3a3a5e",
                        foreground=COULEUR_TEXTE, font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", COULEUR_ACCENT)])

        colonnes = ("id", "titre", "prix_depart", "offre", "vendeur")
        self._tableau = ttk.Treeview(frame_actives, columns=colonnes,
                                     show="headings", height=12)
        for col, texte, largeur in [
            ("id", "ID enc.", 60), ("titre", "Titre", 180),
            ("prix_depart", "Prix départ", 100), ("offre", "Offre actuelle", 120),
            ("vendeur", "Vendeur", 160),
        ]:
            self._tableau.heading(col, text=texte)
            self._tableau.column(col, width=largeur, anchor="center")
        self._tableau.pack(fill="both", expand=True)
        self._tableau.bind("<<TreeviewSelect>>", self._on_selection_active)

        # --- Onglet Historique (enchères terminées)
        frame_histo = tk.Frame(self._notebook, bg=COULEUR_FOND)
        self._notebook.add(frame_histo, text="Historique")

        self._tableau_histo = ttk.Treeview(frame_histo,
            columns=("id", "titre", "vendeur", "gagnant", "prix_final"),
            show="headings", height=12)
        self._tableau_histo.heading("id", text="ID enchère")
        self._tableau_histo.heading("titre", text="Titre")
        self._tableau_histo.heading("vendeur", text="Vendeur")
        self._tableau_histo.heading("gagnant", text="Gagnant")
        self._tableau_histo.heading("prix_final", text="Prix final")
        self._tableau_histo.column("id", width=80, anchor="center")
        self._tableau_histo.column("titre", width=180)
        self._tableau_histo.column("vendeur", width=150)
        self._tableau_histo.column("gagnant", width=150)
        self._tableau_histo.column("prix_final", width=100, anchor="center")
        self._tableau_histo.pack(fill="both", expand=True)

        # ── Colonne droite (scrollable) ──────────────────────────────────────
        col_droite = tk.Frame(corps, bg=COULEUR_FOND, padx=16)
        col_droite.pack(side="right", fill="y")

        # Canvas avec scrollbar pour que tout tienne
        canvas = tk.Canvas(col_droite, bg=COULEUR_FOND, highlightthickness=0)
        scrollbar = tk.Scrollbar(col_droite, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame intérieur qui contiendra toutes les actions
        inner = tk.Frame(canvas, bg=COULEUR_FOND)
        canvas.create_window((0, 0), window=inner, anchor="nw", width=canvas.winfo_reqwidth())

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # Ajuster la largeur du canvas quand la fenêtre change
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(1, width=e.width))

        label(inner, "Actions", police=POLICE_SOUS_TITRE).pack(anchor="w", pady=(0, 12))

        # ── Mise en vente ────────────────────────────────────────────────────
        carte_vente = tk.Frame(inner, bg=COULEUR_SURFACE, padx=14, pady=12)
        carte_vente.pack(fill="x", pady=(0, 12))

        label_surface(carte_vente, "Mettre en vente",
                      police=("Segoe UI", 11, "bold"),
                      couleur=COULEUR_ACCENT2).pack(anchor="w", pady=(0, 8))

        for attr, texte in [("_titre", "Titre"), ("_desc", "Description"),
                             ("_prix", "Prix départ (FCFA)"), ("_duree", "Durée (tours)")]:
            label_surface(carte_vente, texte, police=POLICE_SMALL,
                          couleur=COULEUR_SOUS_TEXT).pack(anchor="w")
            champ = tk.Entry(carte_vente, width=22)
            style_champ(champ)
            champ.pack(fill="x", ipady=4, pady=(0, 4))
            setattr(self, attr, champ)

        self._msg_vente = tk.StringVar()
        tk.Label(carte_vente, textvariable=self._msg_vente, fg=COULEUR_DANGER,
                 bg=COULEUR_SURFACE, font=POLICE_SMALL).pack()

        btn_vente = tk.Button(carte_vente, text="Mettre en vente",
                              command=self._mettre_en_vente)
        style_bouton(btn_vente, COULEUR_ACCENT2)
        btn_vente.pack(fill="x", pady=(6, 0))

        # ── Faire une mise ───────────────────────────────────────────────────
        carte_mise = tk.Frame(inner, bg=COULEUR_SURFACE, padx=14, pady=12)
        carte_mise.pack(fill="x", pady=(0, 12))

        label_surface(carte_mise, "Faire une mise",
                      police=("Segoe UI", 11, "bold"),
                      couleur=COULEUR_ACCENT).pack(anchor="w", pady=(0, 8))

        label_surface(carte_mise, "ID enchère sélectionné :",
                      police=POLICE_SMALL, couleur=COULEUR_SOUS_TEXT).pack(anchor="w")
        self._var_id_enc = tk.StringVar(value="— sélectionnez une ligne —")
        tk.Label(carte_mise, textvariable=self._var_id_enc,
                 font=("Segoe UI", 10, "bold"), fg=COULEUR_ACCENT,
                 bg=COULEUR_SURFACE).pack(anchor="w", pady=(0, 6))

        label_surface(carte_mise, "Montant (FCFA)",
                      police=POLICE_SMALL, couleur=COULEUR_SOUS_TEXT).pack(anchor="w")
        self._champ_montant = tk.Entry(carte_mise, width=22)
        style_champ(self._champ_montant)
        self._champ_montant.pack(fill="x", ipady=4, pady=(0, 4))

        self._msg_mise = tk.StringVar()
        tk.Label(carte_mise, textvariable=self._msg_mise, fg=COULEUR_DANGER,
                 bg=COULEUR_SURFACE, font=POLICE_SMALL).pack()

        btn_mise = tk.Button(carte_mise, text="Placer la mise",
                             command=self._placer_mise)
        style_bouton(btn_mise)
        btn_mise.pack(fill="x", pady=(6, 0))

        # ── Clôturer ─────────────────────────────────────────────────────────
        btn_cloturer = tk.Button(inner, text="Clôturer l'enchère sélectionnée",
                                 command=self._cloturer)
        style_bouton(btn_cloturer, COULEUR_DANGER)
        btn_cloturer.pack(fill="x", pady=(0, 10))

        # Remplir les données
        self._rafraichir()
        # Lier le changement d'onglet pour réinitialiser la sélection
        self._notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _rafraichir(self):
        """Recharge la liste des enchères actives et l'historique."""
        # --- Enchères actives
        for row in self._tableau.get_children():
            self._tableau.delete(row)

        actifs = [o for o in self.app.plateforme.objets.values()
              if o.est_disponible()]

        for o in actifs:
            enc = next(
            (e for e in self.app.plateforme.encheres.values()
             if e.id_objet == o.id and not e.est_cloturee),
            None
            )
            id_enc = str(enc.id) if enc else "-"
            offre  = f"{enc.montant_actuel:.0f} F" if enc else "-"
        # Plus de iid pour éviter "Item - already exists"
        self._tableau.insert("", "end",
                             values=(id_enc, o.titre,
                                     f"{o.prix_depart:.0f} F",
                                     offre, o.vendeur))

        # --- Historique (enchères clôturées)
        for row in self._tableau_histo.get_children():
            self._tableau_histo.delete(row)

        for e in self.app.plateforme.encheres.values():
            if e.est_cloturee:
                obj = self.app.plateforme.objets.get(e.id_objet)
                if obj is None:
                    continue
                gagnant = getattr(e, "gagnant", None)
                if not gagnant:
                    meilleure = getattr(e, "meilleure_offre", None)
                    if meilleure and hasattr(meilleure, "utilisateur"):
                        gagnant = meilleure.utilisateur.email if hasattr(meilleure.utilisateur, "email") else str(meilleure.utilisateur)
                    else:
                        gagnant = "—"
                prix_final = f"{e.montant_actuel:.0f} F" if e.montant_actuel > 0 else "—"
                self._tableau_histo.insert("", "end", values=(
                    e.id, obj.titre, obj.vendeur, gagnant, prix_final
                ))

        # Mettre à jour le solde
        u = self.app.plateforme.utilisateur_connecte
        self._var_solde.set(f"{u.solde:.0f} FCFA")

    def _on_selection_active(self, _event):
        """Met à jour l'ID enchère quand l'utilisateur clique sur une ligne active."""
        sel = self._tableau.selection()
        if sel and self._notebook.index(self._notebook.select()) == 0:
        # Récupère la première colonne (ID enchère) de la ligne sélectionnée
            values = self._tableau.item(sel[0], "values")
            id_enc = values[0] if values else "— sélectionnez une ligne —"
            self._var_id_enc.set(id_enc)
        else:
            self._var_id_enc.set("— sélectionnez une ligne —")

    def _on_tab_changed(self, _event):
        """Quand on change d'onglet, on efface la sélection active."""
        if self._notebook.index(self._notebook.select()) != 0:
            self._var_id_enc.set("— sélectionnez une ligne —")
        else:
            # Si on revient à l'onglet actives, on restaure la sélection si elle existe
            sel = self._tableau.selection()
            if sel:
                self._var_id_enc.set(sel[0])

    def _mettre_en_vente(self):
        self._msg_vente.set("")
        try:
            prix  = float(self._prix.get().strip())
            duree = int(self._duree.get().strip()) if self._duree.get().strip().isdigit() else 1
            self.app.plateforme.deposer_objet(
                self._titre.get().strip(),
                self._desc.get().strip(),
                prix, duree
            )
            for champ in (self._titre, self._desc, self._prix, self._duree):
                champ.delete(0, "end")
            self._rafraichir()
            messagebox.showinfo("✓ Succès", "Objet mis en vente avec succès !")
        except ValueError:
            self._msg_vente.set("Prix et durée doivent être des nombres.")
        except (ChampVideError, PrixInvalideError) as e:
            self._msg_vente.set(str(e))

    def _placer_mise(self):
        self._msg_mise.set("")
        # Vérifier qu'on est bien sur l'onglet actives
        if self._notebook.index(self._notebook.select()) != 0:
            self._msg_mise.set("Veuillez sélectionner l'onglet 'Enchères actives'")
            return
        id_enc_str = self._var_id_enc.get()
        if not id_enc_str.isdigit():
            self._msg_mise.set("Sélectionnez une enchère dans le tableau.")
            return
        try:
            montant = float(self._champ_montant.get().strip())
            self.app.plateforme.placer_mise(int(id_enc_str), montant)
            self._champ_montant.delete(0, "end")
            self._rafraichir()
            messagebox.showinfo("✓ Succès", f"Mise de {montant:.0f} FCFA acceptée !")
        except ValueError:
            self._msg_mise.set("Entrez un montant valide.")
        except (EnchereIntrouvableError, EnchereClotureeError,
                VendeurEncheritError, SoldeInsuffisantError,
                MiseTropBasseError) as e:
            self._msg_mise.set(str(e))

    def _cloturer(self):
        if self._notebook.index(self._notebook.select()) != 0:
            messagebox.showwarning("Attention", "Veuillez sélectionner l'onglet 'Enchères actives'")
            return
        id_enc_str = self._var_id_enc.get()
        if not id_enc_str.isdigit():
            messagebox.showwarning("Attention", "Sélectionnez une enchère dans le tableau.")
            return
        try:
            resultat = self.app.plateforme.cloturer_enchere(int(id_enc_str))
            self._rafraichir()
            if resultat["vendu"]:
                messagebox.showinfo("✓ Clôturée",
                    f"Gagnant : {resultat['gagnant']}\n"
                    f"Montant : {resultat['montant_final']:.0f} FCFA")
            else:
                messagebox.showinfo("✓ Clôturée", "Aucune offre — objet non vendu.")
        except (EnchereIntrouvableError, EnchereClotureeError) as e:
            messagebox.showerror("Erreur", str(e))
        except PermissionError as e:
            messagebox.showerror("Action non autorisée", str(e))
        except Exception as e:
            messagebox.showerror("Erreur inattendue", str(e))

    def _deconnecter(self):
        self.app.plateforme.deconnecter()
        self.app.afficher(EcranAccueil)


# ══════════════════════════════════════════════════════════════════════════════
# Lancement
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()