# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 02:17:03 2025

@author: victor
"""

import pandas as pd

df2015 = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/Todos los años con Tabula/tabula-2015 (1).csv")
df2016 = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/Todos los años con Tabula/tabula-2016.csv")
df2017 = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/Todos los años con Tabula/tabula-2017.csv")
df2018 = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/Todos los años con Tabula/tabula-2018.csv")
df2019 = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/Todos los años con Tabula/tabula-2019.csv")
df2020 = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/2020/df2020_ready.csv")
df2021 = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/Todos los años con Tabula/tabula-2021.pdf.csv")



def limpiar_tabla(df, year):
    """
    Limpia una tabla de turismo del DOT para los años 2015–2021.
    Pasos:
    1. Añade nombres estándar a las columnas.
    2. Limpia caracteres invisibles, espacios y comas.
    3. Convierte columnas a numéricas excepto COUNTRY.
    4. Calcula JAN-DEC sumando los meses.
    5. Ordena por total anual.
    6. Deja solo las primeras 52 filas.
    7. Añade columna YEAR.
    """

    # ==========================================================
    # 1. Nombres de columnas estándar
    # ==========================================================
    columns = (
        "COUNTRY OF RESIDENCE","JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE",
        "JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER","JAN-DEC"
    )
    df.columns = columns  # los PDFs 2015–2021 tienen las mismas columnas

    # ==========================================================
    # 2. Limpiar valores no numéricos (menos COUNTRY)
    # ==========================================================
    for col in df.columns:
        if col == "COUNTRY OF RESIDENCE":
            continue  # no tocamos la columna de nombres de países

        for i in range(len(df)):
            valor = df.at[i, col]

            if isinstance(valor, str):
                # Quitar basura típica de PDF
                valor = valor.replace("\xa0", "")
                valor = valor.replace("\r", "")
                valor = valor.replace("\n", "")
                valor = valor.replace("\t", "")

                # Quitar comas (separador de miles)
                valor = valor.replace(",", "")

                # Quitar espacios
                valor = valor.strip()
                valor = valor.replace(" ", "")

                df.at[i, col] = valor

    # ==========================================================
    # 3. Convertir columnas numéricas a número
    # ==========================================================
    columnas_numericas = [c for c in df.columns if c != "COUNTRY OF RESIDENCE"]

    for col in columnas_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # ==========================================================
    # 4. Reparar JAN-DEC sumando los 12 meses (más seguro)
    # ==========================================================
    meses = [
        "JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE",
        "JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"
    ]
    df["JAN-DEC"] = df[meses].sum(axis=1)

    # ==========================================================
    # 5. Ordenar por JAN-DEC (descendente)
    # ==========================================================
    df = df.sort_values("JAN-DEC", ascending=False).reset_index(drop=True)

    # ==========================================================
    # 6. Top 52 países
    # ==========================================================
    df = df.head(52).reset_index(drop=True)

    # Quitamos la fila 0 (Overseas Filipinos suele quedar allí)
    df = df.drop(index=0).reset_index(drop=True)

    # ==========================================================
    # 7. Añadir YEAR
    # ==========================================================
    df["YEAR"] = year

    return df

df2015_clean = limpiar_tabla(df2015, 2015)
df2016_clean = limpiar_tabla(df2016, 2016)
df2017_clean = limpiar_tabla(df2017, 2017)
df2018_clean = limpiar_tabla(df2018, 2018)
df2019_clean = limpiar_tabla(df2019, 2019)
df2020_clean = limpiar_tabla(df2020, 2020)
df2021_clean = limpiar_tabla(df2021, 2021)



# =============================================================================
# VAMOS A CONCATENAR TODOS LOS DF LIMPIOS
# =============================================================================

df_master15_21 = pd.concat([df2015_clean, df2016_clean,df2017_clean,df2018_clean,df2019_clean,df2020_clean,df2021_clean],ignore_index = True )


#Guardamos la tabla master
df_master15_21.to_csv("df_master15_21_1.csv", index=False, encoding="utf-8-sig")


