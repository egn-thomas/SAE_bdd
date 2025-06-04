import pandas as pd
from sqlalchemy import create_engine

host = "localhost"
port = "5432"
db = "sae_bdd_climat"
user = "user1"
password = "user1"

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

import matplotlib.pyplot as plt

def comparer_co2_vs_pollution_sol(df_co2, df_sol):
    # Préparation des données CO2
    df_co2_agg = df_co2.groupby("annee")["emmission_co2_t"].sum().reset_index()
    df_co2_agg.rename(columns={"emmission_co2_t": "co2_total"}, inplace=True)

    # Préparation des données sol (on suppose que pollution = concentration_polluant_mg_kg)
    df_sol["annee"] = pd.to_datetime(df_sol["date_cas"]).dt.year
    df_sol_agg = df_sol.groupby("annee")["concentration_polluant_mg_kg"].mean().reset_index()
    df_sol_agg.rename(columns={"concentration_polluant_mg_kg": "pollution_moyenne_sol"}, inplace=True)

    # Fusion des deux séries sur les années
    print("Années CO2 :", sorted(df_co2_agg["annee"].unique()))
    print("Années Pollution sol :", sorted(df_sol_agg["annee"].unique()))
    df_comparatif = pd.merge(df_co2_agg, df_sol_agg, on="annee", how="inner")
    print(df_comparatif)
    print(df_comparatif.info())

    # Tracé du graphique
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel("Année")
    ax1.set_ylabel("Émissions CO₂ _t", color="tab:blue")
    ax1.plot(df_comparatif["annee"], df_comparatif["co2_total"], label="CO₂ Total", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Pollution des sols (mg/kg)", color="tab:red")
    ax2.plot(df_comparatif["annee"], df_comparatif["pollution_moyenne_sol"], label="Pollution des sols", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    plt.title("Émissions CO₂ vs Pollution des sols au fil des années")
    plt.tight_layout()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Chargement des données CO2 (corrigé)
    df_co2 = pd.read_sql("SELECT annee, SUM(emmission_co2_t) AS emmission_co2_t FROM emmission_co2 GROUP BY annee", engine)

    # Chargement des données de pollution des sols
    df_sol = pd.read_sql("SELECT date_cas, concentration_polluant_mg_kg FROM maladie_sol", engine)

    # Comparaison des données
    comparer_co2_vs_pollution_sol(df_co2, df_sol)
