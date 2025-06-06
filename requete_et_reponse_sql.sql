--groupe 8 : Lara Fremy TPB, Timéo Doffagne TPD, Thomas Eugène TPD, Célien Kerckhove TPA

--requete pour créer le graphique du nombre catastrophe par ans par les temperature

SELECT c.annee, COUNT(c.id_catastrophe) AS nombre_de_catastrophes
FROM catastrophe_naturel AS c
GROUP BY annee;
       
--réponse

 annee | nombre_de_catastrophes
-------+------------------------
  1991 |                    146
  1989 |                    119
  1974 |                     50
  1977 |                     88
  1971 |                     48
  1935 |                     13
  2022 |                    234
  2017 |                    230
  1983 |                    150
  2009 |                    214
  1958 |                     18
  1973 |                     48
  2013 |                    182
  2003 |                    235
  1933 |                     10
  1953 |                     25
  1903 |                      9
  1912 |                      6
  1997 |                    185
  1905 |                      8
  2016 |                    204
  2018 |                    225
  1994 |                    164
  1963 |                     37
  2014 |                    197
  1928 |                     17
  1924 |                      6
-- Suite  --

--requete pour créer le graphique du nombre catastrophe par ans par les temperature

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
SELECT '2019', AVG(y2019) FROM variation_temperature;

--réponse

 annee |    variation_temp
-------+----------------------
 2010  |   1.0988678907299603
 1975  | -0.03467946058091287
 1970  |  0.08585498960498963
 2005  |   0.8779134179510439
 2000  |   0.7398769931662864
 2019  |   1.5507033898305085
 1990  |   0.5876144265697967
 1985  |  0.08415304528891204
 2015  |    1.392394491337181
 1995  |   0.6128428961748631
 1965  |  -0.2142296874999998
 1961  |  0.13197550807712358
 1980  |   0.1875088357588359
(13 lignes)

--requete pour créer le graphique sur les emmission de co2 par pays 

SELECT p.nom_pays, SUM(ec.emmission_co2_t) AS co2_moyen
FROM emmission_co2 AS ec
INNER JOIN pays AS p ON ec.id_pays = p.id_pays
WHERE ec.annee >= 1990
GROUP BY p.nom_pays
ORDER BY AVG(ec.emmission_co2_t) DESC;

--réponse

           nom_pays             |   co2_moyen
---------------------------------+---------------
 Chine                           | 3571127691988
 Russie                          | 2828471245957
 Allemagne                       | 2491052106347
 Royaume-Uni                     | 2201760809644
 Japon                           | 1467537260166
 France                          | 1033181152060
 Inde                            |  849170272091
 Ukraine                         |  816495826456
 Canada                          |  778937223251
 Pologne                         |  712013553268
 Italie                          |  577024137350
 Afrique du Sud                  |  448652454098
 Mexique                         |  413773326096
 Australie                       |  395457744332
 Belgique                        |  337941496163
 Espagne                         |  327292300846
 Iran                            |  323679220278
 Kazakhstan                      |  317746795500
 Cor├®e du Sud                   |  303807795929
 Br├®sil                         |  300136332758
 Pays-Bas                        |  286623444363
 Arabie saoudite                 |  261527435002
 Indon├®sie                      |  232579751721
 Roumanie                        |  222932859714
 Turquie                         |  183696123205
 Argentine                       |  181676002386
 Venezuela                       |  170214412267
-- Suite  --

--requete pour créer un grapphique sur l'entierté des emmission de co2 dans le monde par année

SELECT annee, SUM(emmission_co2_t) AS co2_mondial
FROM emmission_co2 AS ec
GROUP BY annee
ORDER BY annee;

--réponse

 annee |  co2_mondial
-------+---------------
  1750 |       9350528
  1751 |      18701056
  1752 |      28055248
  1753 |      37409440
  1754 |      46767296
  1755 |      56128816
  1756 |      66135200
  1757 |      76145248
  1758 |      86158960
  1759 |      96176336
  1760 |     106193712
  1761 |     117167392
  1762 |     128144736
  1763 |     139125744
  1764 |     150110416
  1765 |     161098752
  1766 |     173358496
  1767 |     185621904
  1768 |     197888976
  1769 |     210159712
  1770 |     222434112
  1771 |     236045872
  1772 |     249661296
  1773 |     263280384
  1774 |     276903136
  1775 |     290529552
  1776 |     305566608
-- Suite  --

--requete pour créer le graphique sur la comparaison des emmission entre la Chine, l'Allemagne et la France

SELECT annee, SUM(emmission_co2_t) AS co2_france
FROM emmission_co2 AS ec
INNER JOIN pays AS p ON ec.id_pays = p.id_pays
WHERE p.nom_pays = 'France'
AND annee >= 2000
GROUP BY annee
ORDER BY annee;

--réponse 

 annee | co2_france
-------+-------------
  2000 | 31428626515
  2001 | 31839159871
  2002 | 32245170292
  2003 | 32657116430
  2004 | 33070265266
  2005 | 33485782809
  2006 | 33891544108
  2007 | 34286971771
  2008 | 34674963614
  2009 | 35043594804
  2010 | 35420170456
  2011 | 35773905400
  2012 | 36129836915
  2013 | 36487373830
  2014 | 36813259566
  2015 | 37143169942
  2016 | 37476748688
  2017 | 37813744277
  2018 | 38136116165
  2019 | 38452046901
  2020 | 38728680794
(21 lignes)

--requete pour créer le graphique sur la comparaison des emmission entre la Chine, l'Allemagne et la France

SELECT annee, SUM(emmission_co2_t) AS co2_allemagne
FROM emmission_co2 AS ec
INNER JOIN pays AS p ON ec.id_pays = p.id_pays
WHERE p.nom_pays = 'Allemagne'
AND annee >= 2000
GROUP BY annee
ORDER BY annee;

--réponse

 annee | co2_allemagne
-------+---------------
  2000 |   76216668477
  2001 |   77133316999
  2002 |   78033288398
  2003 |   78934440301
  2004 |   79821529428
  2005 |   80688226652
  2006 |   81566547082
  2007 |   82418171411
  2008 |   83273098556
  2009 |   84063393275
  2010 |   84896342383
  2011 |   85705559302
  2012 |   86519543956
  2013 |   87350997794
  2014 |   88143585564
  2015 |   88939195779
  2016 |   89739882411
  2017 |   90525765329
  2018 |   91279876936
  2019 |   91991304745
  2020 |   92635615097
(21 lignes)

--requete pour créer le graphique sur la comparaison des emmission entre la Chine, l'Allemagne et la France


SELECT annee, SUM(emmission_co2_t) AS co2_chine
FROM emmission_co2 AS ec
INNER JOIN pays AS p ON ec.id_pays = p.id_pays
WHERE p.nom_pays = 'Chine'
AND annee >= 2000
GROUP BY annee
ORDER BY annee;

--réponse 

 annee |  co2_chine
-------+--------------
  2000 |  74884032894
  2001 |  78398966689
  2002 |  82271561986
  2003 |  86816575872
  2004 |  92040330528
  2005 |  97916885868
  2006 | 104000000000
  2007 | 111000000000
  2008 | 119000000000
  2009 | 127000000000
  2010 | 135000000000
  2011 | 145000000000
  2012 | 155000000000
  2013 | 165000000000
  2014 | 175000000000
  2015 | 184000000000
  2016 | 194000000000
  2017 | 204000000000
  2018 | 214000000000
  2019 | 225000000000
  2020 | 236000000000
(21 lignes)

--requete pour la corélation entre les nombre de malades par rapport aux nombre de polluant dans le sol

SELECT extract(year from date_cas) AS annee, extract(month from date_cas) AS mois, COUNT(id_cas) AS nombre_malade
FROM maladie_sol 
GROUP BY annee, mois
ORDER BY annee, mois;

--réponse

annee | mois | nombre_malade
-------+------+---------------
  2023 |    4 |           104
  2023 |    5 |           125
  2023 |    6 |           120
  2023 |    7 |           146
  2023 |    8 |           120
  2023 |    9 |           108
  2023 |   10 |           118
  2023 |   11 |           140
  2023 |   12 |           134
  2024 |    1 |           126
  2024 |    2 |           114
  2024 |    3 |           124
  2024 |    4 |           141
  2024 |    5 |           122
  2024 |    6 |           123
  2024 |    7 |           135
  2024 |    8 |           127
  2024 |    9 |           116
  2024 |   10 |           124
  2024 |   11 |           122
  2024 |   12 |           123
  2025 |    1 |           109
  2025 |    2 |           126
  2025 |    3 |           129
  2025 |    4 |            23
(25 lignes)

--requete pour la corélation entre les nombre de malades par rapport aux nombre de polluant dans le sol

SELECT extract(year from date_cas) AS annee, extract(month from date_cas) AS mois, SUM(concentration_polluant_mg_kg) AS concentration_polluant_mg_kg
FROM maladie_sol 
GROUP BY annee, mois
ORDER BY annee, mois;

--réponse 

 annee | mois | concentration_polluant_mg_kg
-------+------+------------------------------
  2023 |    4 |           10662.990000000002
  2023 |    5 |           12245.939999999999
  2023 |    6 |           11228.850000000002
  2023 |    7 |           13771.759999999997
  2023 |    8 |           11466.030000000002
  2023 |    9 |           12046.069999999996
  2023 |   10 |                     11978.78
  2023 |   11 |           14959.480000000007
  2023 |   12 |           13792.970000000001
  2024 |    1 |                     13940.58
  2024 |    2 |           11760.480000000003
  2024 |    3 |           12743.359999999993
  2024 |    4 |           14893.739999999998
  2024 |    5 |           12029.369999999997
  2024 |    6 |           13058.089999999998
  2024 |    7 |           14091.320000000002
  2024 |    8 |           12228.059999999994
  2024 |    9 |           12091.690000000004
  2024 |   10 |           13588.550000000003
  2024 |   11 |           12480.300000000001
  2024 |   12 |           12157.280000000002
  2025 |    1 |           11775.220000000001
  2025 |    2 |           13535.439999999997
  2025 |    3 |           13270.500000000005
  2025 |    4 |                       2266.8
(25 lignes)
