# NBA Analytics & Machine Learning Non Supervisé (Projet ANDO 2026)

Projet d'Analyse de Données (ANDO) — Année Universitaire 2026.

## 🏀 Thème & Sujet
> **Sujet :** *La révolution du tir à 3 points et l'obsolescence des 5 postes traditionnels en NBA : Analyse Factorielle et Classification Non Supervisée des Nouveaux Archétypes de Joueurs.*

### Problématique Centrale
> **« À l'ère du tir à 3 points, dans quelle mesure les 5 postes historiques de la NBA sont-ils devenus obsolètes, et quels nouveaux profils de joueurs émergent lorsque l'on analyse leurs données réelles de jeu ? »**

---

## 📊 Les 3 Piliers Méthodologiques ANDO

1. **Inférence & Modélisation Statistique** :
   - Tests d'hypothèses (ANOVA / Kruskal-Wallis) sur la diffusion spatiale du tir extérieur (`3PAr`) à travers les postes déclarés.
   - Régression linéaire multiple (OLS) modélisant l'impact global (`BPM`) à partir des métriques de possession et d'efficacité, avec diagnostics des résidus (Shapiro-Wilk, Breusch-Pagan, VIF).
2. **Méthode Factorielle (ACP Normée)** :
   - Réduction dimensionnelle sur les statistiques avancées normalisées (`USG%`, `TS%`, `3PAr`, `AST%`, `TRB%`, `BLK%`, `STL%`, `TOV%`).
   - Analyse du cercle des corrélations, éboulis des valeurs propres et projection des joueurs dans le premier plan factoriel.
3. **Clustering Non Supervisé (K-Means & CAH)** :
   - Classification appliquée sur les coordonnées des composantes principales retenues de l'ACP.
   - Optimisation du nombre de classes $k$ (méthode du coude, coefficient de Silhouette, dendrogramme de Ward).
   - Découverte des nouveaux archétypes de jeu (*3-and-D*, *Playmaking Big*, *Primary Scorer*, *Rim Protector*) et comparaison avec les postes historiques via matrice de contingence.

---

## 📂 Structure du Répertoire

```text
.
├── download_and_clean_data.py    # Script de récupération et de nettoyage des données (Basketball-Reference)
├── explore_data.py               # Script d'analyse exploratoire et de génération des figures
├── export_fiche_html.py          # Script de compilation de la fiche intermédiaire en HTML autonome
│
├── nba_2023_2024_cleaned.csv     # Jeu de données consolidé et nettoyé (385 joueurs x 50 variables)
├── nba_2024_advanced_raw.csv     # Données brutes Advanced 2023-2024
├── nba_2024_per_game_raw.csv     # Données brutes Per Game 2023-2024
│
├── eda_correlation_heatmap.png   # Figure 1 : Matrice de corrélation des métriques avancées
├── eda_3pt_by_position.png       # Figure 2 : Boxplots 3PAr par poste officiel
├── eda_ts_vs_usg.png             # Figure 3 : Compromis Usage (USG%) vs Efficacité (TS%)
│
├── FICHE_INTERMEDIAIRE.md        # Fiche intermédiaire de cadrage (2-3 pages, due le 30 nov.)
├── FICHE_INTERMEDIAIRE.html      # Rendu HTML avec images embarquées (prêt pour export PDF)
├── RECAP_PROJET_ANDO.md          # Guide de référence complet du projet
└── README.md                     # Présentation générale du projet
```

---

## 🚀 Reproduction et Exécution

1. **Installation des dépendances :**
   ```bash
   pip install numpy pandas matplotlib seaborn scikit-learn scipy markdown-it-py
   ```

2. **Récupération et nettoyage des données :**
   ```bash
   python download_and_clean_data.py
   ```

3. **Génération des graphiques exploratoires :**
   ```bash
   python explore_data.py
   ```

4. **Export de la fiche intermédiaire en HTML/PDF :**
   ```bash
   python export_fiche_html.py
   ```
