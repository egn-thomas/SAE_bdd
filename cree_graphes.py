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

def comparer_temperature_catastrophe(df_delta_temp_par_an, df_nbcatastrophe_par_an, top_n):
    df_nbcatastrophe_par_an["annee"] = df_nbcatastrophe_par_an["annee"].astype(str)
    df_delta_temp_par_an["annee"] = df_delta_temp_par_an["annee"].astype(str)

    df_merged = pd.merge(df_nbcatastrophe_par_an, df_delta_temp_par_an, on="annee", how="inner")
    df_merged.sort_values("annee", inplace=True)

    print(df_delta_temp_par_an)
    print(df_nbcatastrophe_par_an)


    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Année")
    ax1.set_ylabel("Nombre de catastrophes", color="tab:blue")
    ax1.bar(df_merged["annee"], df_merged["nombre_de_catastrophes"], color="#13AD1A", alpha=0.6)
    ax1.tick_params(axis='y', labelcolor="#13AD1A")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Variation de température (°C)", color="tab:red")
    ax2.plot(df_merged["annee"], df_merged["variation_temp"], color="#042E0B", marker="o")
    ax2.tick_params(axis='y', labelcolor="#042E0B")

    plt.title("Nombre de catastrophes vs Variation de température moyenne")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
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

    comparer_temperature_catastrophe(df_delta_temp_par_an, df_nbcatastrophe_par_an, 15)
    comparer_nbmalade_pollution(df_maladie_par_pays, df_emmission_par_pays, 15)
