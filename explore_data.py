"""
Script d'Analyse Exploratoire des Données (EDA) - NBA 2023-2024
Génère les figures et tableaux pour la fiche intermédiaire de cadrage (2-3 pages)
Projet ANDO 2026
"""

import sys
import os
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

PROJET_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(PROJET_DIR, "nba_2023_2024_cleaned.csv")

def main():
    df = pd.read_csv(DATA_PATH)
    print(f"Chargement du jeu de données : {df.shape[0]} joueurs, {df.shape[1]} variables.")
    
    # Configuration esthétique des graphiques
    sns.set_theme(style="whitegrid", font_scale=1.1)
    
    # -------------------------------------------------------------------------
    # 1. Figure 1 : Matrice de corrélation (Heatmap) des variables avancées
    # -------------------------------------------------------------------------
    advanced_vars = ['USG%', 'TS%', '3PAr', 'AST%', 'TRB%', 'STL%', 'BLK%', 'TOV%', 'BPM']
    corr_matrix = df[advanced_vars].corr()
    
    plt.figure(figsize=(9, 7))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmin=-0.8, vmax=0.8, annot=True, fmt=".2f",
                square=True, linewidths=.5, cbar_kws={"shrink": .8})
    plt.title("Matrice de Corrélation des Métriques Avancées (NBA 2023-2024)", fontsize=13, pad=15)
    plt.tight_layout()
    fig1_path = os.path.join(PROJET_DIR, "eda_correlation_heatmap.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"-> Figure 1 sauvegardée : {fig1_path}")
    
    # -------------------------------------------------------------------------
    # 2. Figure 2 : Boxplot de la fréquence de tir à 3 points (3PAr) par poste
    # -------------------------------------------------------------------------
    plt.figure(figsize=(8, 6))
    order = ['PG', 'SG', 'SF', 'PF', 'C']
    palette = sns.color_palette("muted", 5)
    sns.boxplot(x='Pos', y='3PAr', data=df, order=order, palette=palette)
    sns.stripplot(x='Pos', y='3PAr', data=df, order=order, color='black', alpha=0.35, jitter=0.2, size=5)
    plt.title("Fréquence des Tirs à 3 Points (3PAr) selon le Poste Officiel", fontsize=13, pad=15)
    plt.xlabel("Poste Déclaré", fontsize=11)
    plt.ylabel("3-Point Attempt Rate (3PAr = 3PA / FGA)", fontsize=11)
    plt.tight_layout()
    fig2_path = os.path.join(PROJET_DIR, "eda_3pt_by_position.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"-> Figure 2 sauvegardée : {fig2_path}")
    
    # -------------------------------------------------------------------------
    # 3. Figure 3 : Volume d'Usage (USG%) vs Efficacité (TS%)
    # -------------------------------------------------------------------------
    plt.figure(figsize=(9, 6))
    sns.scatterplot(
        data=df,
        x='USG%',
        y='TS%',
        hue='Pos',
        hue_order=order,
        palette=palette,
        s=70,
        alpha=0.85,
        edgecolor='k'
    )
    plt.axvline(df['USG%'].median(), color='gray', linestyle='--', alpha=0.6, label='Médiane USG%')
    plt.axhline(df['TS%'].median(), color='gray', linestyle=':', alpha=0.6, label='Médiane TS%')
    
    # Mettre en valeur quelques joueurs emblématiques
    notable_players = ['Luka Dončić', 'Nikola Jokić', 'Stephen Curry', 'Rudy Gobert', 'Victor Wembanyama']
    for p in notable_players:
        row = df[df['Player'] == p]
        if not row.empty:
            plt.annotate(
                p,
                (row['USG%'].values[0], row['TS%'].values[0]),
                textcoords="offset points",
                xytext=(6, 6),
                ha='left',
                fontsize=9,
                fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", fc="yellow", alpha=0.5, ec="none")
            )
            
    plt.title("Compromis Volume d'Usage (USG%) vs Efficacité au Tir (TS%)", fontsize=13, pad=15)
    plt.xlabel("Usage Percentage (USG%)", fontsize=11)
    plt.ylabel("True Shooting Percentage (TS%)", fontsize=11)
    plt.legend(title="Poste", bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    fig3_path = os.path.join(PROJET_DIR, "eda_ts_vs_usg.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"-> Figure 3 sauvegardée : {fig3_path}")
    
    print("\nEDA terminée avec succès. Toutes les visualisations sont prêtes dans le dossier Projet/.")

if __name__ == "__main__":
    main()
