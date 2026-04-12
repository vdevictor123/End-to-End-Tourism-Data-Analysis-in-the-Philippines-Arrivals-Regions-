# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 09:23:21 2026

@author: victor
"""

import pandas as pd

# =============================================================================
# PASO 1 — Cargar el archivo
# =============================================================================

df = pd.read_excel("C:/Users/victor/Desktop/Nueva carpeta (2)/Excel/regions_master_2015_2023_01.xlsx")

print("Shape (filas, columnas):", df.shape)
print("Columnas:", df.columns.tolist())
print("Años disponibles:", sorted(df["Year"].unique()))
print("Valores únicos en Level:", df["Level"].unique())


# =============================================================================
# PASO 2 — Detectar locations con Level inconsistente
# =============================================================================
# groupby agrupa todas las filas por Location
# nunique() cuenta cuántos valores DISTINTOS tiene "Level" para cada Location
# Si una Location tiene más de 1 Level distinto → hay inconsistencia

niveles_por_location = df.groupby("Location")["Level"].nunique()
locations_problematicas = niveles_por_location[niveles_por_location > 1]

print(f"\nLocations con Level inconsistente: {len(locations_problematicas)}")

# Ver el detalle de cada location problemática: qué Level tiene en cada año
for loc in locations_problematicas.index:
    levels = df[df["Location"] == loc]["Level"].unique()
    años_por_level = df[df["Location"] == loc].groupby("Level")["Year"].apply(list).to_dict()
    print(f"  {loc}: {años_por_level}")


# =============================================================================
# PASO 3 — Aplicar la corrección
# =============================================================================
# Regla: si una Location aparece como "City/Municipality" en CUALQUIER año,
# entonces es una ciudad real → corregir todos sus años a "City/Municipality"
#
# Excepción: Region VIII y Region IX son regiones reales.
# En 2017-2018 aparecieron mal clasificadas como City/Municipality o Province,
# pero deben mantenerse como "Region".

# Obtener la lista de todas las locations que alguna vez fueron City/Municipality
locations_ciudad = df[df["Level"] == "City/Municipality"]["Location"].unique()

# Función que se aplica fila por fila:
# Si la Location de esa fila está en la lista de ciudades → asigna City/Municipality
# Si no → deja el Level original
def corregir_level(row):
    if row["Location"] in locations_ciudad:
        return "City/Municipality"
    return row["Level"]

# apply() recorre cada fila y ejecuta la función
df["Level_Clean"] = df.apply(corregir_level, axis=1)

# Corregir las excepciones: Region VIII y IX deben volver a "Region"
regiones_reales = ["Region IX (ZAMBOANGA PENINSULA)", "Region VIII (EASTERN VISAYAS)"]
df.loc[df["Location"].isin(regiones_reales), "Level_Clean"] = "Region"


# =============================================================================
# PASO 4 — Verificar que la corrección funcionó
# =============================================================================

print("\n=== VERIFICACIÓN LAPU-LAPU ===")
lapu = df[df["Location"].str.contains("Lapu", case=False, na=False)]
print(lapu[["Year", "Location", "Level", "Level_Clean"]])

print("\n=== VERIFICACIÓN CEBU CITY ===")
cebu = df[df["Location"] == "Cebu City"]
print(cebu[["Year", "Location", "Level", "Level_Clean"]])

# Comprobar que ya no queda ninguna location inconsistente
niveles_final = df.groupby("Location")["Level_Clean"].nunique()
restantes = niveles_final[niveles_final > 1]
if len(restantes) == 0:
    print("\n✓ Ninguna location tiene Level inconsistente. Corrección completada.")
else:
    print(f"\n⚠ Aún hay {len(restantes)} locations inconsistentes:")
    print(restantes)


# =============================================================================
# PASO 5 — Añadir columnas de Latitude y Longitude por Region_Code
# =============================================================================
# Estas coordenadas representan el centroide geográfico de cada región.
# Se usan para posicionar las regiones en el mapa de Power BI.
# Cada fila hereda las coordenadas de su Region_Code correspondiente.

REGION_COORDINATES = {
    "NCR":         (14.5995, 120.9842),
    "CAR":         (17.3510, 121.1720),
    "Region I":    (16.0832, 120.6200),
    "Region II":   (17.6132, 121.7270),
    "Region III":  (15.4755, 120.5960),
    "Region IV-A": (14.1008, 121.0794),
    "Region IV-B": (10.7202, 121.0794),
    "Region V":    (13.4213, 123.4136),
    "Region VI":   (11.0050, 122.5373),
    "Region VII":  (10.3157, 123.8854),
    "Region VIII": (11.2440, 125.0039),
    "Region IX":   ( 8.1527, 123.2577),
    "Region X":    ( 8.0220, 124.6220),
    "Region XI":   ( 7.3041, 125.6800),
    "Region XII":  ( 6.2700, 124.6860),
    "Region XIII": ( 8.9456, 125.5450),
}

# map() busca cada Region_Code en el diccionario y asigna lat/lon
# lambda extrae el primer valor (índice 0) para Latitude
# lambda extrae el segundo valor (índice 1) para Longitude
# Si un Region_Code no está en el diccionario → devuelve None
df["Latitude"]  = df["Region_Code"].map(lambda x: REGION_COORDINATES.get(x, (None, None))[0])
df["Longitude"] = df["Region_Code"].map(lambda x: REGION_COORDINATES.get(x, (None, None))[1])

# Verificar que no hay regiones sin coordenadas
sin_coords = df[df["Latitude"].isna()]["Region_Code"].unique()
if len(sin_coords) == 0:
    print("\n✓ Todas las regiones tienen coordenadas asignadas.")
else:
    print(f"\n⚠ Regiones sin coordenadas: {sin_coords}")


# =============================================================================
# PASO 6 — Guardar el archivo limpio
# =============================================================================
# Conservamos el Level original renombrado como "Level_Original"
# para poder comparar con el Level corregido.
# El orden de columnas queda: ..., Level_Original, Level_Clean, ...

df = df.rename(columns={"Level": "Level_Original", "Level_Clean": "Level"})

df.to_excel("regions_master_LIMPIO_01.xlsx", index=False)

print(f"\n✓ Archivo guardado como: regions_master_LIMPIO.xlsx")
print(f"  Filas totales: {len(df)}")
print(f"  Columnas: {df.columns.tolist()}")