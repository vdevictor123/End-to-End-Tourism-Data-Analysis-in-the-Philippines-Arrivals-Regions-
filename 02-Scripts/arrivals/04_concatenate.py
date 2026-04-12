# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 10:24:02 2025

@author: victor
"""

import pandas as pd

df_master1 = pd.read_csv("C:/Users/victor/Desktop/filipinas/estudio turimos filipinas/df_master15_21_1.csv")
df_master2 = pd.read_csv("C:/Users/victor/Desktop/filipinas/estudio turimos filipinas/Visitor Arrivals to the Philippines/Todos los años con Tabula/df par concatenar/df_master22_23.csv")



#ERROR porque el los valores de la columna 
#master = pd.concat([master1,master2], ignore_index = True)


sorted(df_master1["COUNTRY OF RESIDENCE"].unique())

sorted(df_master2["COUNTRY OF RESIDENCE"].unique())

df_master1.columns

columns_m1 = ['COUNTRY OF RESIDENCE', 'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY',
       'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER',
       'DECEMBER', 'JAN-DEC', 'YEAR']

df_master2.columns = columns_m1


map_nat_to_country = {
    # nacionalidades → países
    "AMERICAN": "USA",
    "AUSTRALIAN": "AUSTRALIA",
    "AUSTRIAN": "AUSTRIA",
    "BANGLADESHI": "BANGLADESH",
    "BELGIAN": "BELGIUM",
    "BRAZILIAN": "BRAZIL",
    "BRITISH": "UNITED KINGDOM",
    "BRUNEIAN": "BRUNEI",
    "BURMESE": "MYANMAR",
    "CANADIAN": "CANADA",
    "CHINESE": "CHINA",
    "CZECH": "CZECH REPUBLIC",
    "DANISH": "DENMARK",
    "DUTCH": "NETHERLANDS",
    "EMIRATI": "UNITED ARAB EMIRATES",
    "FINNISH": "FINLAND",
    "FRENCH": "FRANCE",
    "GERMAN": "GERMANY",
    "GUAMANIAN": "GUAM",
    "HONG KONGER": "HONG KONG",   # <- mejor así
    "INDIAN": "INDIA",
    "INDONESIAN": "INDONESIA",
    "IRISH": "IRELAND",
    "ISRAELI": "ISRAEL",
    "ITALIAN": "ITALY",           # <- aquí estaba el error
    "JAPANESE": "JAPAN",
    "KUWAITI": "KUWAIT",
    "MALAYSIAN": "MALAYSIA",
    "MEXICAN": "MEXICO",
    "MONGOLIAN": "MONGOLIA",
    "NEPALESE": "NEPAL",
    "NIGERIAN": "NIGERIA",
    "NORWEGIAN": "NORWAY",
    "PAKISTANI": "PAKISTAN",
    "POLISH": "POLAND",
    "PORTUGUESE": "PORTUGAL",
    "ROMANIAN": "ROMANIA",
    "RUSSIAN": "RUSSIAN FEDERATION",  # o "RUSSIA" si lo quieres más simple
    "SAUDI ARABIAN": "SAUDI ARABIA",
    "SINGAPOREAN": "SINGAPORE",
    "SOUTH AFRICAN": "SOUTH AFRICA",
    "SOUTH KOREAN": "KOREA",
    "SPANISH": "SPAIN",
    "SWEDISH": "SWEDEN",
    "SWISS": "SWITZERLAND",
    "TAIWANESE": "TAIWAN",
    "THAI": "THAILAND",
    "TURKISH": "TURKEY",
    "VIETNAMESE": "VIETNAM",

    # errores tipográficos / casos especiales
    "rSOUTH KOREA": "KOREA",
    "TOTAL OVERSEAS FILIPINOS *": "OVERSEAS FILIPINOS",
    "OVERSEAS FILIPINOS*": "OVERSEAS FILIPINOS",
    "OVERSEAS FILIPINOS***": "OVERSEAS FILIPINOS",
    "VERSEAS FILIPINOS***": "OVERSEAS FILIPINOS",
}

map_nat_to_country.update({
    "HONGKONG": "HONG KONG",
    "HONG KONG": "HONG KONG",
    "HONG KONG - SAR": "HONG KONG",

    "MACAU - SAR": "MACAU",

    "QATAR*": "QATAR",

    "* OVERSEAS FILIPINOS": "OVERSEAS FILIPINOS",

    "NEW ZEALANDER": "NEW ZEALAND",

    "RSOUTH KOREA": "KOREA",

    "UNITED STATES OF AMERICA": "USA",

    "TOTAL (CIS & RUSSIA)": "CIS",
    "INDEPENDENT STATES": "CIS",
})




df_master2["COUNTRY OF RESIDENCE"] = (
    df_master2["COUNTRY OF RESIDENCE"]
    .str.upper().str.strip()
    .replace(map_nat_to_country)
)

df_master1["COUNTRY OF RESIDENCE"] = (
    df_master1["COUNTRY OF RESIDENCE"]
    .str.upper().str.strip()
    .replace(map_nat_to_country)
)


val1 = set(df_master1["COUNTRY OF RESIDENCE"].unique())
val2 = set(df_master2["COUNTRY OF RESIDENCE"].unique())

solo_en_1 = sorted(val1 - val2)
solo_en_2 = sorted(val2 - val1)

print("Solo en df_master1:")
print(solo_en_1)

print("\nSolo en df_master2:")
print(solo_en_2)






df_master = pd.concat([df_master1, df_master2], ignore_index = True)

df_master["COUNTRY OF RESIDENCE"] = df_master["COUNTRY OF RESIDENCE"].replace({"RUSSIAN FEDERATION": "RUSSIA"})

df_master[df_master["COUNTRY OF RESIDENCE"] == "RUSSIAN FEDERATION"]

df_master[df_master["COUNTRY OF RESIDENCE"] == "CIS"]

df_master = df_master[df_master["COUNTRY OF RESIDENCE"] != "CIS"].copy()


df_master.to_csv("df_master_2015_2023.csv",index=False, encoding="utf-8-sig")
















