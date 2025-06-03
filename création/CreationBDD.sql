-- création BDD
CREATE DATABASE sae_bdd_climat;

\c sae_bdd_climat

-- création pays
CREATE TABLE pays (
	id_pays INT PRIMARY KEY,
	nom_pays VARCHAR(50) UNIQUE
);

	
-- création variation_temperature
CREATE TABLE variation_temperature (
	id_pays INT,
	mois INT,
	Y1961 FLOAT,
	Y1962 FLOAT,
	Y1963 FLOAT,
	Y1964 FLOAT,
	Y1965 FLOAT,
	Y1966 FLOAT,
	Y1967 FLOAT,
	Y1968 FLOAT,
	Y1969 FLOAT,
	Y1970 FLOAT,
	Y1971 FLOAT,
	Y1972 FLOAT,
	Y1973 FLOAT,
	Y1974 FLOAT,
	Y1975 FLOAT,
	Y1976 FLOAT,
	Y1977 FLOAT,
	Y1978 FLOAT,
	Y1979 FLOAT,
	Y1980 FLOAT,
	Y1981 FLOAT,
	Y1982 FLOAT,
	Y1983 FLOAT,
	Y1984 FLOAT,
	Y1985 FLOAT,
	Y1986 FLOAT,
	Y1987 FLOAT,
	Y1988 FLOAT,
	Y1989 FLOAT,
	Y1990 FLOAT,
	Y1991 FLOAT,
	Y1992 FLOAT,
	Y1993 FLOAT,
	Y1994 FLOAT,
	Y1995 FLOAT,
	Y1996 FLOAT,
	Y1997 FLOAT,
	Y1998 FLOAT,
	Y1999 FLOAT,
	Y2000 FLOAT,
	Y2001 FLOAT,
	Y2002 FLOAT,
	Y2003 FLOAT,
	Y2004 FLOAT,
	Y2005 FLOAT,
	Y2006 FLOAT,
	Y2007 FLOAT,
	Y2008 FLOAT,
	Y2009 FLOAT,
	Y2010 FLOAT,
	Y2011 FLOAT,
	Y2012 FLOAT,
	Y2013 FLOAT,
	Y2014 FLOAT,
	Y2015 FLOAT,
	Y2016 FLOAT,
	Y2017 FLOAT,
	Y2018 FLOAT,
	Y2019 FLOAT,
	CONSTRAINT fk_pays FOREIGN KEY (id_pays) REFERENCES pays(id_pays)
);
	
	-- création catastrophe_naturel
CREATE TABLE catastrophe_naturel (
    id_catastrophe INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    annee INT,
    nom_pays VARCHAR(100),
    groupe_catastrophe VARCHAR(100),
    type_catastrophe VARCHAR(100),
    sous_type_catastrophe VARCHAR(100),
    nombre_catastrophe INT,
    total_mort INT,
    "degat_total(USD)" BIGINT,
    "degat_total_reel(USD)" BIGINT
);

-- création maladie_sol
CREATE TABLE maladie_sol (
    id_cas varchar(50) PRIMARY KEY,
    date_cas DATE,
    id_pays INT,
    type_polluant VARCHAR(50),
    concentration_polluant_mg_kg FLOAT,
    ph_sol FLOAT,
    temperature_c FLOAT,
    proportion_mat_organique FLOAT,
    type_maladie VARCHAR(100),
    severite_maladie VARCHAR(50),
    symptome_maladie VARCHAR(100),
    guerison BOOLEAN,
    FOREIGN KEY (id_pays) REFERENCES pays(id_pays)
);

-- création emission_co2
CREATE TABLE emmission_co2 (
    id_pays INT,
    annee INT,
    "emmission_co2(T)" FLOAT,
    population_2022 FLOAT,
    aire FLOAT,
    pourcentage_monde FLOAT,
    densite_km FLOAT,
    FOREIGN KEY (id_pays) REFERENCES pays(id_pays)
);
