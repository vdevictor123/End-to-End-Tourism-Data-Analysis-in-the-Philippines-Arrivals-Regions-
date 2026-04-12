import pandas as pd

# =============================================================================
# PASO 1 — Cargar el archivo
# =============================================================================

df = pd.read_excel("regions_master_2015_2023_01.xlsx")

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
# PASO 5 — Guardar el archivo limpio
# =============================================================================
# Reemplazamos la columna "Level" original con la corregida
# y eliminamos la columna temporal "Level_Clean"

df["Level"] = df["Level_Clean"]
df = df.drop(columns=["Level_Clean"])

df.to_excel("regions_master_LIMPIO.xlsx", index=False)

print(f"\n✓ Archivo guardado como: regions_master_LIMPIO.xlsx")
print(f"  Filas totales: {len(df)}")
print(f"  Columnas: {df.columns.tolist()}")
