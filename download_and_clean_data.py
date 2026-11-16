"""
Script de récupération et de préparation des données NBA (Basketball-Reference)
Projet : Analyse de Données (ANDO) 2026
Thème  : Sport - NBA Analytics & Clustering des profils de joueurs
"""

import sys
import os
import io
import requests
import numpy as np
import pandas as pd

# Configuration encodage console Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

PROJET_DIR = os.path.dirname(os.path.abspath(__file__))
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_table(url: str) -> pd.DataFrame:
    """Télécharge une page Basketball-Reference et extrait le tableau principal."""
    print(f"Téléchargement : {url} ...")
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    dfs = pd.read_html(io.StringIO(response.text))
    # Le premier tableau est la table principale des joueurs
    df = dfs[0]
    return df

def clean_bbr_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie un tableau brut issu de Basketball-Reference."""
    # 1. Supprimer les en-têtes répétés dans le tableau HTML
    df_clean = df[df['Player'] != 'Player'].copy()
    
    # 2. Supprimer la colonne 'Rk' (rang)
    if 'Rk' in df_clean.columns:
        df_clean = df_clean.drop(columns=['Rk'])
        
    # 3. Traiter les joueurs transférés en cours de saison :
    # Si un joueur a joué pour plusieurs équipes, Basketball-Reference insère une ligne 'TOT' (Total)
    # puis une ligne par équipe. On garde en priorité la ligne 'TOT' pour avoir la saison complète du joueur.
    def select_best_row(group):
        if 'TOT' in group['Team'].values:
            return group[group['Team'] == 'TOT'].iloc[0]
        return group.iloc[0]
    
    # Regrouper par nom de joueur
    df_clean = df_clean.groupby('Player', as_index=False, group_keys=False).apply(select_best_row)
    
    # 4. Standardiser les postes multiples (ex: "PG-SG" -> "PG")
    df_clean['Pos'] = df_clean['Pos'].apply(lambda x: str(x).split('-')[0] if pd.notnull(x) else x)
    
    return df_clean

def main():
    print("=" * 70)
    print("RÉCUPÉRATION DES DONNÉES NBA 2023-2024")
    print("=" * 70)
    
    # 1. Téléchargement des stats avancées (Advanced)
    url_advanced = "https://www.basketball-reference.com/leagues/NBA_2024_advanced.html"
    df_adv_raw = fetch_table(url_advanced)
    raw_adv_path = os.path.join(PROJET_DIR, "nba_2024_advanced_raw.csv")
    df_adv_raw.to_csv(raw_adv_path, index=False)
    print(f"-> Stats avancées brutes sauvegardées ({df_adv_raw.shape[0]} lignes) dans {raw_adv_path}")
    
    # 2. Téléchargement des stats par match (Per Game)
    url_per_game = "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
    df_pg_raw = fetch_table(url_per_game)
    raw_pg_path = os.path.join(PROJET_DIR, "nba_2024_per_game_raw.csv")
    df_pg_raw.to_csv(raw_pg_path, index=False)
    print(f"-> Stats par match brutes sauvegardées ({df_pg_raw.shape[0]} lignes) dans {raw_pg_path}")
    
    # 3. Nettoyage des deux tables
    df_adv = clean_bbr_dataframe(df_adv_raw)
    df_pg = clean_bbr_dataframe(df_pg_raw)
    
    print(f"\nAprès dédoublonnage des joueurs transférés :")
    print(f"  Joueurs uniques dans Advanced : {len(df_adv)}")
    print(f"  Joueurs uniques dans Per Game : {len(df_pg)}")
    
    # 4. Fusion des deux tables sur les identifiants clés
    common_cols = ['Player', 'Pos', 'Age', 'Team', 'G', 'GS']
    cols_to_drop_from_pg = [c for c in common_cols if c != 'Player']
    df_pg_subset = df_pg.drop(columns=[c for c in cols_to_drop_from_pg if c in df_pg.columns])
    
    # Renommer MP dans per_game en MP_per_game pour éviter la confusion avec MP total de advanced
    if 'MP' in df_pg_subset.columns:
        df_pg_subset = df_pg_subset.rename(columns={'MP': 'MP_per_game'})
    
    df_merged = pd.merge(df_adv, df_pg_subset, on='Player', how='inner')
    print(f"-> Table fusionnée : {df_merged.shape[0]} joueurs, {df_merged.shape[1]} variables")
    
    # 5. Conversion des types numériques
    categorical_cols = ['Player', 'Pos', 'Team', 'Awards']
    for col in df_merged.columns:
        if col not in categorical_cols:
            df_merged[col] = pd.to_numeric(df_merged[col], errors='coerce')
            
    # 6. Filtrage pour l'analyse statistique rigoureuse :
    # Retirer les joueurs avec un temps de jeu trop faible (MP < 400 minutes sur la saison)
    min_minutes = 400
    df_filtered = df_merged[df_merged['MP'] >= min_minutes].copy()
    
    # Imputer ou gérer les éventuels NaN dans les pourcentages (ex: si un joueur n'a tiré aucun 3 points, 3P% peut être NaN -> 0.0)
    pct_cols = ['3P%', '2P%', 'FT%', 'FG%', 'eFG%']
    for p in pct_cols:
        if p in df_filtered.columns:
            df_filtered[p] = df_filtered[p].fillna(0.0)
            
    # Supprimer d'éventuelles colonnes vides d'artefacts HTML
    df_filtered = df_filtered.dropna(axis=1, how='all')
    
    # 7. Sauvegarde du dataset consolidé final
    final_path = os.path.join(PROJET_DIR, "nba_2023_2024_cleaned.csv")
    df_filtered.to_csv(final_path, index=False)
    print(f"\n=> Jeu de données nettoyé et consolidé sauvegardé avec succès !")
    print(f"   Chemin : {final_path}")
    print(f"   Effectif final retenu : {df_filtered.shape[0]} joueurs (avec MP >= {min_minutes} min)")
    print(f"   Nombre de variables conservées : {df_filtered.shape[1]}")
    
    # 8. Affichage d'un aperçu statistique des variables clés
    key_vars = ['Age', 'MP', 'PTS', 'TRB', 'AST', 'USG%', 'TS%', '3PAr', 'AST%', 'TRB%', 'BLK%', 'BPM']
    available_keys = [k for k in key_vars if k in df_filtered.columns]
    print("\n" + "=" * 70)
    print("RÉSUMÉ STATISTIQUE DES VARIABLES CLÉS")
    print("=" * 70)
    print(df_filtered[available_keys].describe().round(2))
    
    # Répartition par poste
    print("\nRépartition des joueurs par poste officiel :")
    print(df_filtered['Pos'].value_counts())

if __name__ == "__main__":
    main()
