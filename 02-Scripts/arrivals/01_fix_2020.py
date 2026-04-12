# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 03:11:49 2025

@author: victor
"""

import pandas as pd


df2020_14 = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/2020/tabula-2020_14Filas(ok).csv")
df2020_15_limpiar = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/2020/tabula-2020_15Filas(limpiar).csv")

#Recuperamos los datos a la columna correspondiente (estan switch)
df2020_15_limpiar.columns

filas = range(8,12)
col1= "-"
col2 = 'Unnamed: 5'

for i in filas:
    temp = df2020_15_limpiar.at[i,col1]
    df2020_15_limpiar.at[i, col1] = df2020_15_limpiar.at[i,col2]
    df2020_15_limpiar.at[i, col2] = temp

filas = [26]
col1= "-"
col2 = 'Unnamed: 5'

for i in filas:
    temp = df2020_15_limpiar.at[i,col1]
    df2020_15_limpiar.at[i, col1] = df2020_15_limpiar.at[i,col2]
    df2020_15_limpiar.at[i, col2] = temp   

filas = range(29,31)
col1= "-"
col2 = 'Unnamed: 5'

for i in filas:
    temp = df2020_15_limpiar.at[i,col1]
    df2020_15_limpiar.at[i, col1] = df2020_15_limpiar.at[i,col2]
    df2020_15_limpiar.at[i, col2] = temp   
   
    
filas = [32]
col1= 'Unnamed: 5'
col2 = '1'

for i in filas:
    temp = df2020_15_limpiar.at[i,col1]
    df2020_15_limpiar.at[i, col1] = df2020_15_limpiar.at[i,col2]
    df2020_15_limpiar.at[i, col2] = temp
    

#Drop fake column
df2020_15_limpiar= df2020_15_limpiar.drop(columns = "Unnamed: 5")


# Antes de juntar las tablas les añadiremos una fila con el nombre de las columnas
#Para luego juntarlas y asi obtener df2020 limpio y listo para utilizar 

columns1 = ( "COUNTRY OF RESIDENCE","JANUARY","FEBRUARY", "MARCH","APRIL", "MAY", "JUNE", "JULY", "AGUST", "SETEMBER","OCTOBER","NOVEMBER", "DESEMBER",
           "JAN-DEC")


#Cargamos el df con otro nombre para no pisar el original
df2020_14_COPY = pd.read_csv("C:/Users/victor/Desktop/FILIPINAS/Estudio Turimos Filipinas/Visitor Arrivals to the Philippines/2020/tabula-2020_14Filas(ok).csv")

df2020_14_COPY.columns

#Extraemos los datos de la fila de los nombres de las columnas
old_cols = df2020_14_COPY.columns.tolist()

#Renombramos los nombres de las columnas
df2020_14_COPY.columns =  columns1

#Creamos una nueva fila con los valores de China anteriormente extraidos
header_row = pd.DataFrame([old_cols], columns=columns1)


df2020_14 = pd.concat([header_row, df2020_14_COPY], ignore_index=True)


# =============================================================================
# Vamos a hacer lo mismo pero con df2020_15_limpiar
# =============================================================================

#Creamos copia
df2020_15_limpiar_COPY = df2020_15_limpiar

#nombes columnas
df2020_15_limpiar_COPY.columns

#Extraemosdatosde la fiala de los "nombres de las columnas"
old_columns = df2020_15_limpiar_COPY.columns.tolist()

#Renombramos con los nombres de las columnas que queremos
df2020_15_limpiar_COPY.columns = columns1

#Creamos un df nuevo con los datos que queremos con los nombres col ya cambiados para luego concatenar 
head_row = pd.DataFrame([old_columns], columns = columns1)

#Concatenamos para añadi en indice 0 la fila que antes era "nombres de las columnas"
df2020_15_limpiar = pd.concat([head_row, df2020_15_limpiar_COPY], ignore_index=True)


#Vamos a borrar una fila que esta en nan y se añadio erroneamente al extraer los datos de la tabla del pdf original
df2020_15_limpiar = df2020_15_limpiar.drop(index = 22)


# =============================================================================
# Ahora que tenemos los df limpios los vamos a concatenar 
# =============================================================================

df2020 = pd.concat([df2020_14,df2020_15_limpiar], ignore_index = True)


#Guardamos este df
#df2020.to_csv("df2020_ready.csv", index=False, encoding="utf-8-sig")





