import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np
import random

host = "localhost"
port = "5432"
db = "sae_bdd_climat"
user = "user1"
password = "user1"

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

def comparer_temperature_catastrophe(df_delta_temp_par_an, df_nbcatastrophe_par_an, top_n):

    df_nbcatastrophe_par_an["annee"] = df_nbcatastrophe_par_an["annee"].astype(str)
    df_delta_temp_par_an["annee"] = df_delta_temp_par_an["annee"].astype(str)

    df_merged = pd.merge(df_nbcatastrophe_par_an, df_delta_temp_par_an, on="annee", how="inner")
    df_merged.sort_values("annee", inplace=True)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Année")
    ax1.set_ylabel("Nombre de catastrophes", color="#13AD1A")
    ax1.bar(df_merged["annee"], df_merged["nombre_de_catastrophes"], color="#13AD1A", alpha=0.6)
    ax1.tick_params(axis='y', labelcolor="#13AD1A")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Variation de température (°C)", color="#042E0B")
    ax2.plot(df_merged["annee"], df_merged["variation_temp"], color="#042E0B", marker="o")
    ax2.tick_params(axis='y', labelcolor="#042E0B")

    plt.title("Nombre de catastrophes et variation de température moyenne depuis 1961", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def hausse_du_co2(df_co2_par_pays, top_n=12):

    df_sorted = df_co2_par_pays.sort_values(by="co2_moyen", ascending=False).reset_index(drop=True)

    df_top = df_sorted.head(top_n)
    df_autres = df_sorted.iloc[top_n:]

    autres_total = df_autres["co2_moyen"].sum()

    if autres_total > 0:
        df_autres_row = pd.DataFrame([{
            "nom_pays": "Autres",
            "co2_moyen": autres_total
        }])
        df_top = pd.concat([df_top, df_autres_row], ignore_index=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    couleurs = ["#cfffd7", "#71d381", "#81e091", "#61c572", "#44a554", "#278336", "#1D772C", '#cfffd7', '#71d381', '#81e091', '#61c572', '#44a554', '#278336']
    random.shuffle(couleurs)
    ax.pie(
        df_top["co2_moyen"],
        labels=df_top["nom_pays"],
        autopct='%1.1f%%',
        startangle=140,
        colors=couleurs[:len(df_top)],
        textprops={'fontsize': 12},
    )

    ax.set_title("Répartition des émissions de CO₂ par pays depuis 1990", y=1.05)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def co2_mondial_par_an(df_co2_par_an):

    df_co2_par_an["annee"] = pd.to_datetime(df_co2_par_an["annee"], format='%Y')
    df_co2_par_an.sort_values("annee", inplace=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df_co2_par_an["annee"], df_co2_par_an["co2_mondial"], color="#074111")
    plt.title("Évolution des émissions mondiales de CO₂ par an depuis 1760", fontsize=14)
    plt.xlabel("Année")
    plt.ylabel("Émissions de CO₂ (tonnes)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def graphique_co2_par_pays(df_france, df_allemagne, df_chine):
    plt.figure(figsize=(12, 6))

    plt.plot(df_france["annee"], df_france["co2_france"], label="France", color="#03A51E")
    plt.plot(df_allemagne["annee"], df_allemagne["co2_allemagne"], label="Allemagne", color="#079DB1")
    plt.plot(df_chine["annee"], df_chine["co2_chine"], label="Chine", color="#b61010")

    plt.xlabel("Année")
    plt.ylabel("Émissions de CO₂ (tonnes)")
    plt.title("Évolution des émissions de CO₂ en France, Allemagne et Chine depuis 2000", fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def graphique_temp_vs_co2(df_delta_temp_par_an, df_co2_par_an):
    import matplotlib.pyplot as plt

    # Assurez-vous que les années soient bien des entiers
    df_delta_temp_par_an["annee"] = df_delta_temp_par_an["annee"].astype(int)
    df_co2_par_an["annee"] = df_co2_par_an["annee"].astype(int)

    # Fusionner les deux DataFrames sur l'année
    df_merged = pd.merge(df_delta_temp_par_an, df_co2_par_an, on="annee", how="inner")
    df_merged.sort_values("annee", inplace=True)

    # Création du graphique
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Année")
    ax1.set_ylabel("Variation moyenne de température (°C)", color="#ca3131")
    ax1.plot(df_merged["annee"], df_merged["variation_temp"], color="#ca3131", marker="o", label="Température")
    ax1.tick_params(axis='y', labelcolor="#ca3131")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Émissions mondiales de CO₂ (tonnes)", color="#2ea810")
    ax2.plot(df_merged["annee"], df_merged["co2_mondial"], color="#2ea810", marker="s", label="CO₂ mondial")
    ax2.tick_params(axis='y', labelcolor="#2ea810")

    plt.title("Évolution de la température moyenne et des émissions mondiales de CO₂")
    plt.grid(True)
    plt.tight_layout()
    plt.show()




if __name__ == "__main__":

    df_nbcatastrophe_par_an = pd.read_sql("""
        SELECT c.annee, COUNT(c.id_catastrophe) AS nombre_de_catastrophes
        FROM catastrophe_naturel AS c
        GROUP BY annee;
        """, engine)
    
    df_delta_temp_par_an = pd.read_sql("""
        SELECT '1961' AS annee, AVG(y1961) AS variation_temp FROM variation_temperature
        UNION
        SELECT '1965', AVG(y1965) FROM variation_temperature
        UNION
        SELECT '1970', AVG(y1970) FROM variation_temperature
        UNION
        SELECT '1975', AVG(y1975) FROM variation_temperature
        UNION
        SELECT '1980', AVG(y1980) FROM variation_temperature
        UNION
        SELECT '1985', AVG(y1985) FROM variation_temperature
        UNION
        SELECT '1990', AVG(y1990) FROM variation_temperature
        UNION
        SELECT '1995', AVG(y1995) FROM variation_temperature
        UNION
        SELECT '2000', AVG(y2000) FROM variation_temperature
        UNION
        SELECT '2005', AVG(y2005) FROM variation_temperature
        UNION
        SELECT '2010', AVG(y2010) FROM variation_temperature
        UNION
        SELECT '2015', AVG(y2015) FROM variation_temperature
        UNION
        SELECT '2019', AVG(y2019) FROM variation_temperature
        """, engine)
    
    df_co2_par_pays = pd.read_sql("""
        SELECT p.nom_pays, SUM(ec.emmission_co2_t) AS co2_moyen
        FROM emmission_co2 AS ec
        INNER JOIN pays AS p ON ec.id_pays = p.id_pays
        WHERE ec.annee >= 1990
        GROUP BY p.nom_pays
        ORDER BY AVG(ec.emmission_co2_t) DESC;
        """, engine)
    
    df_co2_par_an = pd.read_sql("""
        SELECT annee, SUM(emmission_co2_t) AS co2_mondial
        FROM emmission_co2 AS ec
        GROUP BY annee
        ORDER BY annee;
        """, engine)
    
    df_co2_par_an_france = pd.read_sql("""
        SELECT annee, SUM(emmission_co2_t) AS co2_france
        FROM emmission_co2 AS ec
        INNER JOIN pays AS p ON ec.id_pays = p.id_pays
        WHERE p.nom_pays = 'France'
        AND annee >= 2000
        GROUP BY annee
        ORDER BY annee;
        """, engine)
    
    df_co2_par_an_allemagne = pd.read_sql("""
        SELECT annee, SUM(emmission_co2_t) AS co2_allemagne
        FROM emmission_co2 AS ec
        INNER JOIN pays AS p ON ec.id_pays = p.id_pays
        WHERE p.nom_pays = 'Allemagne'
        AND annee >= 2000
        GROUP BY annee
        ORDER BY annee;
        """, engine)
    
    df_co2_par_an_chine = pd.read_sql("""
        SELECT annee, SUM(emmission_co2_t) AS co2_chine
        FROM emmission_co2 AS ec
        INNER JOIN pays AS p ON ec.id_pays = p.id_pays
        WHERE p.nom_pays = 'Chine'
        AND annee >= 2000
        GROUP BY annee
        ORDER BY annee;
        """, engine)
    

    
    # comparer_temperature_catastrophe(df_delta_temp_par_an, df_nbcatastrophe_par_an, 15)
    # hausse_du_co2(df_co2_par_pays)
    # co2_mondial_par_an(df_co2_par_an)
    # graphique_co2_par_pays(df_co2_par_an_france, df_co2_par_an_allemagne, df_co2_par_an_chine)
    graphique_temp_vs_co2(df_delta_temp_par_an, df_co2_par_an)


