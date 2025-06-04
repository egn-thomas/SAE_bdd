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

import numpy as np

def comparer_nbmalade_pollution(df_maladie_par_pays, df_emmission_par_pays, top_n):
    # On garde nom_pays uniquement dans l'un des deux DataFrames
    df_emmission_par_pays = df_emmission_par_pays.drop(columns=["nom_pays"])

    # Fusion sur id_pays
    df_merged = pd.merge(df_emmission_par_pays, df_maladie_par_pays, on="id_pays", how="inner")
    print(f"Nombre de pays après fusion : {len(df_merged)}")

    # Tri pour mettre en avant les pays avec le plus de CO2
    df_merged.sort_values("emmission_co2_t", ascending=False, inplace=True)

    # Limiter aux top_n pays
    df_top = df_merged.head(top_n)

    # Positions pour les barres
    x = np.arange(len(df_top))  # positions des pays sur l'axe x
    width = 0.4  # largeur des barres

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Pays")
    ax1.set_ylabel("Émissions CO₂ (tonnes)", color="tab:blue")
    # Barres pour émissions CO2 décalées à gauche (-width/2)
    bars1 = ax1.bar(x - width/2, df_top["emmission_co2_t"], width, color="tab:blue", alpha=0.6, label="CO₂")
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax1.set_xticks(x)
    ax1.set_xticklabels(df_top["nom_pays"], rotation=45, ha="right")

    # Création du second axe y
    ax2 = ax1.twinx()
    ax2.set_ylabel("Nombre de cas de maladies des sols", color="tab:red")
    # Barres pour nombre de cas décalées à droite (+width/2)
    bars2 = ax2.bar(x + width/2, df_top["nombre_de_cas"], width, color="tab:red", label="Cas")
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title("Émissions de CO₂ (2020) vs Cas de maladies des sols (2023) par pays")
    plt.tight_layout()
    plt.grid(True)
    plt.show()


def comparer_temperature_catastrophe(df_delta_temp_par_an, df_nbcatastrophe_par_an, top_n):
    df_nbcatastrophe_par_an["annee"] = df_nbcatastrophe_par_an["annee"].astype(str)
    df_delta_temp_par_an["annee"] = df_delta_temp_par_an["annee"].astype(str)

    df_merged = pd.merge(df_nbcatastrophe_par_an, df_delta_temp_par_an, on="annee", how="inner")
    df_merged.sort_values("annee", inplace=True)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Année")
    ax1.set_ylabel("Nombre de catastrophes", color="tab:blue")
    ax1.bar(df_merged["annee"], df_merged["nombre_de_catastrophes"], color="tab:blue", alpha=0.6)
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel("Variation de température (°C)", color="tab:red")
    ax2.plot(df_merged["annee"], df_merged["variation_temp"], color="tab:red", marker="o")
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title("Nombre de catastrophes vs Variation de température moyenne")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":

    df_emmission_par_pays = pd.read_sql("""
        SELECT p.id_pays, p.nom_pays, SUM(ec.emmission_co2_t) AS emmission_co2_t
        FROM emmission_co2 AS ec
        INNER JOIN pays AS p ON p.id_pays = ec.id_pays
        WHERE ec.annee = 2020
        GROUP BY p.id_pays, p.nom_pays
    """, engine)

    df_maladie_par_pays = pd.read_sql("""
        SELECT p.id_pays, p.nom_pays, COUNT(ms.id_cas) AS nombre_de_cas
        FROM maladie_sol AS ms
        INNER JOIN pays AS p ON p.id_pays = ms.id_pays
        WHERE EXTRACT(YEAR FROM ms.date_cas) = 2023
        GROUP BY p.id_pays, p.nom_pays
    """, engine)

    df_nbcatastrophe_par_an = pd.read_sql("""
        SELECT c.annee, COUNT(c.id_catastrophe) AS nombre_de_catastrophes
        FROM catastrophe_naturel AS c
        GROUP BY annee;        
        """, engine)
    
    df_delta_temp_par_an = pd.read_sql("""
        SELECT 'y1961' AS annee, AVG(y1961) AS variation_temp FROM variation_temperature
        UNION
        SELECT 'y1965', AVG(y1965) FROM variation_temperature
        UNION
        SELECT 'y1970', AVG(y1970) FROM variation_temperature
        UNION
        SELECT 'y1975', AVG(y1975) FROM variation_temperature
        UNION
        SELECT 'y1980', AVG(y1980) FROM variation_temperature
        UNION
        SELECT 'y1985', AVG(y1985) FROM variation_temperature
        UNION
        SELECT 'y1990', AVG(y1990) FROM variation_temperature
        UNION
        SELECT 'y1995', AVG(y1995) FROM variation_temperature
        UNION
        SELECT 'y2000', AVG(y2000) FROM variation_temperature
        UNION
        SELECT 'y2005', AVG(y2005) FROM variation_temperature
        UNION
        SELECT 'y2010', AVG(y2010) FROM variation_temperature
        UNION
        SELECT 'y2015', AVG(y2015) FROM variation_temperature
        UNION
        SELECT 'y2019', AVG(y2019) FROM variation_temperature
        """, engine)

    comparer_temperature_catastrophe(df_delta_temp_par_an, df_nbcatastrophe_par_an, 15)
    comparer_nbmalade_pollution(df_maladie_par_pays, df_emmission_par_pays, 15)
