# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 05:00:55 2025

@author: victor
"""

import pandas as pd


#df2021 = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/2021/tabula-2021.pdf1234.csv", header = None)
df2022 = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/2022/tabula-2022.pdf1234.csv")
df2023 = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/2023/tabula-2023.pdf1234.csv", engine="python", usecols=list(range(15)))
#Estamos modificando la tabla para  que las 3 tengan el mismo formato

#Vamos a dejar solo 14 columanas en cada DF. Nacionalidad y los meses (1+13)


#Añadimos el nombre a las columnas
columns = ( "COUNTRY OF RESIDENCE","JANUARY","FEBRUARY", "MARCH","APRIL", "MAY", "JUNE", "JULY", "AGUST", "SETEMBER","OCTOBER","NOVEMBER", "DESEMBER",
           "JAN-DEC", "% OF","JAN-DEC 2020", "%" )

columns2 = ( "COUNTRY OF RESIDENCE","JANUARY","FEBRUARY", "MARCH","APRIL", "MAY", "JUNE", "JULY", "AGUST", "SETEMBER","OCTOBER","NOVEMBER", "DESEMBER",
           "JAN-DEC", "% OF")

"""

len(columns)
len(df2021.columns)

len(df2023.columns)

#Renombramos las columnas 
df2021.columns = columns
df2023.columns = columns2

# =============================================================================
# Limpieza df2021
# =============================================================================

#Limpiamos el df2021 para que quede con 14 columnas 
       #"COUNTRY OF RESIDENCE"
       #Los 12 meses
       #"JAN-DEC"
#Esta sera la estructura de los 3 df 

df2021.columns
len(df2021.columns)

df2021 = df2021.drop(columns = ['% OF', 'JAN-DEC 2020', '%'])

#Valores nulos o con un "-" los pasamos a 0
df2021.replace("-", 0)
df2021.fillna(0)

#Usamos este comando porque hay espacios raros asi nos aseguramos el cambiar los datos a 0
df2021 = df2021.replace(r"\s*-\s*", 0, regex=True).fillna(0)

# =============================================================================
# Vamos a quitar los espacios que hay dentro de los valores de toda la tabla
# =============================================================================          
            
for col in df2021.columns:
    if col == "COUNTRY OF RESIDENCE":
        continue

    for i in range(len(df2021)):
        valor = df2021.at[i, col]

        if isinstance(valor, str):
            # 1. Quitar basura de PDF
            valor = valor.replace("\xa0", "")
            valor = valor.replace("\r", "")
            valor = valor.replace("\n", "")
            valor = valor.replace("\t", "")

            # 2. Quitar espacios al principio y al final
            valor = valor.strip()

            # 3. Quitar comas (separador de miles)
            valor = valor.replace(",", "")

            # 4. Quitar TODOS los espacios restantes (por si queda alguno suelto)
            valor = valor.replace(" ", "")

            df2021.at[i, col] = valor           
            
                        

#Pasamos todas la columnas a numerico menos la primera que debe ser object (que son los nombres de los paises)

columnas_numericas = [c for c in df2021.columns if c != "COUNTRY OF RESIDENCE"]

for col in columnas_numericas:
    df2021[col] = pd.to_numeric(df2021[col], errors="coerce").fillna(0)


columnas_numericas= []

for col in df2021.columns:
    if col != "COUNTRY OF RESIDENCE":
        columnas_numericas.append(col)

for col in columnas_numericas:
    df2021[col] = pd.to_numeric(df2021[col], errors= "coerce").fillna(0)

#Comprobamos
df2021.info()


#Ordenamos de mayor a menor
df2021 = df2021.sort_values("JAN-DEC", ascending=False).reset_index(drop=True)

#nos quedamos solo con los primeros 50 paises (tambien overseas filipinos son una gran masa y se considera oportuno añadirlos )
df2021= df2021.head(52).reset_index(drop = True)

df2021 = df2021.drop(index=0).reset_index(drop=True)

"""

# =============================================================================
# Limpieza df2022
# =============================================================================

#Le falta January como columna con valores 0
        #Esto es debido a que ese año en Enero el pais se cerro a los turistas por un virus en el pais
#Añadimos "JANUARY" con valores 0

df2022.columns

#Ahora si que podemos añadir la columna y hemos solucionado un problema
df2022.insert(loc= df2022.columns.get_loc('Total\rFebruary 2022'), column= "JANUARY", value = 0)
        

#Lo que vamos a hacer es cambiar primero los nombres de las columnas excuyendo "January"
#y luego lo insertamos
len(df2022.columns)
columns3 = ( "COUNTRY OF RESIDENCE","JANUARY","FEBRUARY", "MARCH","APRIL", "MAY", "JUNE", "JULY", "AGUST", "SETEMBER","OCTOBER","NOVEMBER", "DESEMBER",
           "JAN-DEC", "% OF")

df2022.columns = columns3



#Vamos a quitar la ultima columna asi quedara con 14 columnas

df2022 = df2022.drop(columns = ('% OF'))
len(df2022.columns)


#Vamos a limpiar todos los valores y los vamos a convertir a int/float (como en la tabla anterior)

#Cleaning
for col in df2022.columns:
    if col == "COUNTRY OF RESIDENCE":
        continue
    
    for i in range(len(df2022)):
        valor = df2022.at[i, col]
        
        if isinstance(valor, str):
            valor = valor.replace("\xa0", "")
            valor = valor.replace("\r", "")
            valor = valor.replace("\n", "")
            valor = valor.replace("\t", "")
            valor = valor.replace(",", "")
            valor = valor.replace(" ", "")
            valor = valor.replace("**", "")
            valor = valor.strip()

            df2022.at[i,col] = valor
            
#Convert
columnas_numericas = []

for col in df2022.columns:
    if col != "COUNTRY OF RESIDENCE":
        columnas_numericas.append(col)



for col in columnas_numericas:
    df2022[col] = pd.to_numeric(df2022[col], errors="coerce").fillna(0)


#Eliminar la primera fila (no nos sirve pq es extra)

df2022 = df2022.drop(index=2).reset_index(drop=True)
df2022 = df2022.drop(index=0).reset_index(drop=True)

df2022 = df2022.sort_values("JAN-DEC", ascending=False).reset_index(drop=True)

df2022 = df2022.head(51).reset_index(drop=True)

year = 2022 

df2022["YEAR"] = year

# =============================================================================
# Limpeza df2023
# =============================================================================

len(df2023.columns)
df2023.columns

df2023.columns = columns2

#Eliminamos la ultima columna para obtener 14 columnas
df2023= df2023.drop(columns = ("% OF"))

#Eliminamos la primera fila
df2023 = df2023.drop(index = [0,1]).reset_index(drop=True)
df2023 = df2023.drop(index = 1).reset_index(drop=True)

#Limpiamos valores 
for col in df2023.columns:
    if col == "COUNTRY OF RESIDENCE":
        continue
    
    for i in range(len(df2023)):
        valor = df2023.at[i,col]
    
        if isinstance(valor, str):
            valor = valor.replace("\xa0", "")
            valor = valor.replace("\r", "")
            valor = valor.replace("\n", "")
            valor = valor.replace("\t", "")
            valor = valor.replace(",", "")
            valor = valor.replace(" ", "")
            valor = valor.replace("**", "")
            valor = valor.strip()

            df2023.at[i,col] = valor


columnas_numericas = []

for col in df2023.columns:
    if col != "COUNTRY OF RESIDENCE":       
        columnas_numericas.append(col)
    

for col in columnas_numericas:
    df2023[col] = pd.to_numeric(df2023[col], errors= "coerce").fillna(0)
    

#Nos quedamos solo con las filas 51
df2023= df2023.head(51).reset_index(drop= True)

year = 2023

df2023["YEAR"] = year


#Concatenamos las tablas

df_master22_23 = pd.concat([df2022,df2023], ignore_index = True)



#Guardamos la tabla master22_23

df_master22_23.to_csv("df_master22_23.csv", index=False, encoding="utf-8-sig")











