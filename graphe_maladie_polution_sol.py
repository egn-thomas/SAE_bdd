import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np

host = "localhost"
port = "5432"
db = "sae_bdd_climat"
user = "user1"
password = "user1"

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

def comparer_malade_polluant_sol(df_polluant_sol_par_mois, df_cas_malade_par_mois, top_n):
    df_cas_malade_par_mois["mois_annee"] = df_cas_malade_par_mois["annee"].astype(str) + "-" + df_cas_malade_par_mois["mois"].astype(str)
    df_polluant_sol_par_mois["mois_annee"] = df_polluant_sol_par_mois["annee"].astype(str) + "-" + df_polluant_sol_par_mois["mois"].astype(str)

    df_merged = pd.merge(df_cas_malade_par_mois, df_polluant_sol_par_mois, on="mois_annee", how="inner")
    df_merged.sort_values("mois_annee", inplace=True)

    # Vérification du nombre de lignes
    print(df_merged.shape)  # Devrait afficher (24, X)

    # Affichage des données
    print(df_polluant_sol_par_mois.head())
    print(df_cas_malade_par_mois.head())

    # Création du graphique
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Mois-Annee")
    ax1.set_ylabel("Nombre Malade", color="#13AD1A")
    ax1.bar(df_merged["mois_annee"], df_merged["nombre_malade"], color="#13AD1A", alpha=0.3)
    ax1.tick_params(axis='y', labelcolor="#13AD1A")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Concentration Polluant", color="#0B3A13F7")
    ax2.plot(df_merged["mois_annee"], df_merged["concentration_polluant_mg_kg"], color="#0B3A13F7", marker="o")
    ax2.tick_params(axis='y', labelcolor="#0B3A13F7")

    plt.title("nombre de malade vs Polluant dans le sol")
    plt.xticks(rotation=45, fontsize=2)
    ax1.set_xticks(ax1.get_xticks()[::3])
    ax1.set_xlabel("Mois-Annee", fontsize=8)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    df_cas_malade_par_mois = pd.read_sql("""
        SELECT extract(year from date_cas) AS annee, extract(month from date_cas) AS mois, COUNT(id_cas) AS nombre_malade
        FROM maladie_sol 
        GROUP BY annee, mois
        ORDER BY annee, mois;
    """, engine)

    df_polluant_sol_par_mois = pd.read_sql("""
        SELECT extract(year from date_cas) AS annee, extract(month from date_cas) AS mois, SUM(concentration_polluant_mg_kg) AS concentration_polluant_mg_kg
        FROM maladie_sol 
        GROUP BY annee, mois
        ORDER BY annee, mois;
    """, engine)

    comparer_malade_polluant_sol(df_polluant_sol_par_mois, df_cas_malade_par_mois, 15)
