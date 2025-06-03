import pandas as pd
from sqlalchemy import create_engine

# ⚠️ Remplace les valeurs ci-dessous par les tiennes
host = "localhost"
port = "5432"
db = "sae_bdd_climat"
user = "user1"
password = "user1"

# Connexion via SQLAlchemy
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

# Lire une table PostgreSQL → DataFrame
df = pd.read_sql("SELECT * FROM emmission_co2", engine)

print(df.head())