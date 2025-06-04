import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

host = "localhost"
port = "5432"
db = "sae_bdd_climat"
user = "user1"
password = "user1"

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

def comparer_nbmalade_pollution(df_maladie_par_pays, df_emmission_par_pays):
    # Fusion des deux DataFrames sur l'identifiant du pays
    df_merged = pd.merge(df_emmission_par_pays, df_maladie_par_pays, on="id_pays", how="inner")

    # Tri pour mettre en avant les pays avec le plus de cas
    df_merged.sort_values("nombre_de_cas", ascending=False, inplace=True)

    # Limiter le graphique aux 15 premiers pays pour plus de lisibilité
    df_top = df_merged.head(15)

    # Création du graphique à barres avec double axe
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Pays")
    ax1.set_ylabel("Émissions CO₂ (tonnes)", color="tab:blue")
    ax1.bar(df_top["nom_pays"], df_top["emmission_co2_t"], color="tab:blue", alpha=0.6, label="CO₂")
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_xticklabels(df_top["nom_pays"], rotation=45, ha="right")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Nombre de cas de maladies des sols", color="tab:red")
    ax2.plot(df_top["nom_pays"], df_top["nombre_de_cas"], color="tab:red", marker="o", label="Cas")
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title("Émissions de CO₂ (2020) vs Cas de maladies des sols (2023) par pays")
    plt.tight_layout()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":

    df_emmission_par_pays = pd.read_sql("SELECT p.id_pays, p.nom_pays, SUM(ec.emmission_co2_t) AS emmission_co2_t FROM emmission_co2 AS ec INNER JOIN pays AS p ON p.id_pays = ec.id_pays WHERE ec.annee = 2020 GROUP BY id_pays", engine)

    # Chargement des données de pollution des sols
    df_maladie_par_pays = pd.read_sql("SELECT p.id_pays, p.nom_pays, COUNT(id_cas) AS nombre_de_cas FROM maladie_sol AS ms INNER JOIN pays AS p ON p.id_pays = ms.id_pays WHERE EXTRACT(YEAR FROM ms.date_cas) = 2023 GROUP BY id_pays", engine)

    # Comparaison des données
    comparer_nbmalade_pollution(df_maladie_par_pays, df_emmission_par_pays)
