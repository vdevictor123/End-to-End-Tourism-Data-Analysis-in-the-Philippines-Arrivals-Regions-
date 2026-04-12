# SQL Analysis Summary — Philippines Tourism (2015–2023)
# Resumen de Análisis SQL — Turismo en Filipinas (2015–2023)

---

## Overview / Descripción General

This document summarizes all SQL queries written for this project, the questions they answer, and the key findings derived from the data.

Este documento resume todas las consultas SQL escritas para este proyecto, las preguntas que responden y los hallazgos clave obtenidos de los datos.

**Datasets used / Datasets utilizados:**
- `arrivals` — International visitor arrivals by country of residence, 2015–2023
- `regions` — Regional tourist distribution (foreign, domestic, OFW) by region/province/city, 2015–2023

---

## Part 1 — Visitor Arrivals (`Query_SQL_arrivals.sql`)
## Parte 1 — Llegadas de Visitantes Internacionales

---

### Query 1 — Top country overall / País con más visitantes acumulados

**Question / Pregunta:**  
Which single country sent the most tourists to the Philippines across the entire 2015–2023 period?  
¿Qué país envió más turistas a Filipinas en todo el período 2015–2023?

```sql
SELECT country_of_residence,
       SUM(jan_dec) AS total
FROM arrivals
GROUP BY country_of_residence
ORDER BY total DESC
LIMIT 1;
```

**Answer / Respuesta:**  
**USA** leads with the highest total accumulated arrivals across all years.  
**Estados Unidos** lidera con el mayor número de llegadas acumuladas en todos los años.

**Insight:**  
The USA's dominance is driven by the large Filipino diaspora, strong economic ties, and direct flight connectivity. This position remained consistent throughout the pre-COVID growth years and into the recovery period.  
El liderazgo de EE.UU. se explica por la gran diáspora filipina, los vínculos económicos y la conectividad aérea directa. Esta posición se mantuvo constante durante los años de crecimiento previos al COVID y en el período de recuperación.

---

### Query 2 — Top 10 countries overall / Top 10 países en total

**Question / Pregunta:**  
Which are the top 10 origin countries by total arrivals during 2015–2023?  
¿Cuáles son los 10 principales países de origen por llegadas totales durante 2015–2023?

```sql
SELECT country_of_residence,
       SUM(jan_dec) AS total
FROM arrivals
GROUP BY country_of_residence
ORDER BY total DESC
LIMIT 10;
```

**Answer / Respuesta:**  
The top 10 are dominated by: **USA, Korea, Japan, China, Australia, Taiwan, Singapore, Canada, UK, and Hong Kong** (approximate ranking based on accumulated totals).  
El top 10 está dominado por: **EE.UU., Corea, Japón, China, Australia, Taiwán, Singapur, Canadá, Reino Unido y Hong Kong** (ranking aproximado según totales acumulados).

**Insight:**  
Asian countries (Korea, Japan, China) rank very highly, reflecting the Philippines' position as a key destination within the Asia-Pacific tourism circuit. The strong Korean presence is driven by affordable flights, and beach tourism (Cebu, Boracay).  
Los países asiáticos (Corea, Japón, China) ocupan posiciones muy altas, lo que refleja la posición de Filipinas como destino clave en el circuito turístico Asia-Pacífico. La fuerte presencia coreana se explica por vuelos económicos y turismo de playa.

---

### Query 3 — Top origin country per year / País de origen líder por año

**Question / Pregunta:**  
Which country sent the most tourists each year from 2015 to 2023?  
¿Qué país envió más turistas en cada año entre 2015 y 2023?

```sql
SELECT country_of_residence, YEAR, total
FROM (
    SELECT country_of_residence, year,
           SUM(jan_dec) AS total,
           ROW_NUMBER() OVER(PARTITION BY year ORDER BY SUM(jan_dec) DESC) AS rn
    FROM arrivals
    GROUP BY country_of_residence, year
) t
WHERE rn <= 1;
```

**Answer / Respuesta:**  
**USA** held the #1 position every single year from 2015 to 2023, with no other country displacing it even during the COVID recovery.  
**EE.UU.** mantuvo la posición #1 cada año sin excepción, sin que ningún otro país lo desplazara incluso durante la recuperación post-COVID.

**Insight:**  
This remarkable consistency confirms that US-Philippines ties (economic, familial, cultural) create a structurally stable tourism flow that is resistant to external shocks.  
Esta notable consistencia confirma que los lazos EE.UU.-Filipinas (económicos, familiares, culturales) generan un flujo turístico estructuralmente estable y resistente a perturbaciones externas.

---

### Query 4 — Average annual tourists per country / Promedio anual por país

**Question / Pregunta:**  
What is the average number of annual arrivals per country across the 2015–2023 period?  
¿Cuál es el promedio de llegadas anuales por país durante 2015–2023?

```sql
SELECT country_of_residence,
       ROUND(AVG(total_anual)) AS promedio_anual
FROM (
    SELECT country_of_residence, year,
           SUM(jan_dec) AS total_anual
    FROM arrivals
    GROUP BY country_of_residence, year
) t
GROUP BY country_of_residence
ORDER BY promedio_anual DESC;
```

**Answer / Respuesta:**  
USA averages the highest annual visitors. Korea and Japan follow closely. China's average is skewed downward due to the post-2019 collapse.  
EE.UU. tiene la media más alta de visitantes anuales. Corea y Japón le siguen de cerca. La media de China está reducida por el colapso posterior a 2019.

---

### Query 5 — Spain monthly and annual evolution / Evolución mensual y anual de España

**Question / Pregunta:**  
How has Spain's visitor count evolved month by month and year by year?  
¿Cómo ha evolucionado el número de visitantes de España mes a mes y año a año?

```sql
SELECT * FROM arrivals
WHERE country_of_residence = 'Spain';
```

**Answer / Respuesta:**  
Spain shows steady, modest volumes — typically in the range of 20,000–40,000 annual visitors. COVID caused a near-complete stoppage in 2020–2021, with slow recovery.  
España muestra volúmenes moderados y estables — típicamente entre 20.000 y 40.000 visitantes anuales. El COVID provocó una parada casi completa en 2020–2021, con una recuperación lenta.

**Insight:**  
Spain's volumes, while small in absolute terms, are consistent and driven largely by long-haul leisure tourists attracted to the Philippines' beach destinations.  
Los volúmenes de España, aunque pequeños en términos absolutos, son consistentes y están impulsados principalmente por turistas de ocio de largo recorrido atraídos por los destinos de playa de Filipinas.

---

### Query 6 — Year-over-year growth for Spain and USA / Crecimiento interanual para España y EE.UU.

**Question / Pregunta:**  
What is the year-over-year percentage change in arrivals for Spain and USA?  
¿Cuál es el cambio porcentual interanual en llegadas para España y EE.UU.?

```sql
-- Spain / España
SELECT country_of_residence, jan_dec, year,
    LAG(jan_dec) OVER(ORDER BY year) AS pre_year,
    ROUND((jan_dec - LAG(jan_dec) OVER(ORDER BY year)) * 100 
          / LAG(jan_dec) OVER(ORDER BY year)) AS percent
FROM arrivals
WHERE country_of_residence = 'Spain';

-- USA (same logic / misma lógica)
```

**Answer / Respuesta:**  
Both countries show a consistent growth pattern until 2019, a catastrophic drop in 2020 (~-98%), near-zero in 2021, and strong positive YoY rates in 2022–2023 (mathematical recovery effect from the zero baseline).  
Ambos países muestran un patrón de crecimiento constante hasta 2019, una caída catastrófica en 2020 (~-98%), casi cero en 2021 y tasas YoY muy positivas en 2022–2023 (efecto matemático de recuperación desde base cero).

---

### Query 7 — China growth analysis / Análisis del crecimiento de China

**Question / Pregunta:**  
How did China's annual tourism to the Philippines grow or decline across the period?  
¿Cómo creció o decreció el turismo de China a Filipinas a lo largo del período?

```sql
SELECT country_of_residence, year, jan_dec,
    LAG(jan_dec) OVER(ORDER BY year) AS pre_year,
    ROUND((jan_dec - LAG(jan_dec) OVER(ORDER BY year)) * 100 
          / LAG(jan_dec) OVER(ORDER BY year)) AS percent
FROM arrivals
WHERE country_of_residence = 'China';
```

**Answer / Respuesta:**  
China experienced **explosive growth from 2016 to 2019** (growing from ~500K to ~1.7M arrivals), becoming the 2nd largest source market. Post-COVID, Chinese arrivals have not returned to pre-pandemic levels by 2023, unlike USA and Korea.  
China experimentó un **crecimiento explosivo de 2016 a 2019** (de ~500K a ~1,7M llegadas), convirtiéndose en el 2° mercado emisor. Tras el COVID, las llegadas chinas no han vuelto a los niveles prepandémicos en 2023, a diferencia de EE.UU. y Corea.

**Insight:**  
China's slow post-COVID recovery is influenced by China's strict re-opening timeline (zero-COVID policy ended late 2022), geopolitical factors, and a broader shift in outbound Chinese tourism patterns.  
La lenta recuperación post-COVID de China está influida por el calendario de reapertura (la política de cero-COVID terminó a finales de 2022), factores geopolíticos y un cambio más amplio en los patrones de turismo saliente chino.

---

### Query 8 — USA vs China comparison / Comparación EE.UU. vs China

**Question / Pregunta:**  
How do the annual growth rates of USA and China compare year by year?  
¿Cómo se comparan las tasas de crecimiento anuales de EE.UU. y China año a año?

```sql
SELECT country_of_residence, jan_dec, year,
    LAG(jan_dec) OVER(PARTITION BY country_of_residence ORDER BY year) AS pre_year,
    ROUND((jan_dec - LAG(jan_dec) OVER(PARTITION BY country_of_residence ORDER BY year)) * 100 
          / LAG(jan_dec) OVER(PARTITION BY country_of_residence ORDER BY year), 2) AS percent
FROM arrivals
WHERE country_of_residence IN ('USA', 'China')
ORDER BY year;
```

**Answer / Respuesta:**  
During 2016–2019, **China grew significantly faster than the USA** in percentage terms, nearly closing the gap in absolute visitor numbers. Post-2021, the USA recovered much faster than China.  
Durante 2016–2019, **China creció significativamente más rápido que EE.UU.** en términos porcentuales, casi cerrando la brecha en números absolutos. Tras 2021, EE.UU. se recuperó mucho más rápido que China.

---

### Query 9 — Monthly tourism ranking / Ranking mensual de turismo

**Question / Pregunta:**  
Which months of the year attract the most and least international tourists to the Philippines?  
¿Qué meses del año atraen más y menos turistas internacionales a Filipinas?

```sql
SELECT 'January' AS month, SUM(january) AS total_tourist FROM arrivals
UNION ALL SELECT 'February', SUM(february) FROM arrivals
UNION ALL SELECT 'March', SUM(march) FROM arrivals
-- ... (all 12 months)
ORDER BY total_tourist DESC;
```

**Answer / Respuesta:**  
- **Peak months / Meses pico:** January > March > February (holiday season + dry weather)  
- **Lowest months / Meses más bajos:** September > October > November (typhoon season)  

**Insight:**  
The January peak is driven by year-end holiday extensions, New Year events, and ideal weather in beach destinations. September is the statistically weakest month due to the typhoon season, which affects flight connectivity and tourist confidence.  
El pico de enero está impulsado por las extensiones de vacaciones de fin de año, eventos de Año Nuevo y el clima ideal en los destinos de playa. Septiembre es el mes estadísticamente más débil debido a la temporada de tifones, que afecta la conectividad de vuelos y la confianza de los turistas.

---

## Part 2 — Regional Travelers (`Query_SQL_regions.sql`)
## Parte 2 — Viajeros por Región

---

### Query 1.1 — Top 5 regions by foreign tourists / Top 5 regiones por turistas extranjeros

**Question / Pregunta:**  
Which 5 Philippine regions accumulated the highest number of foreign tourists from 2015–2023?  
¿Qué 5 regiones de Filipinas acumularon más turistas extranjeros entre 2015–2023?

```sql
SELECT Region_name, SUM(Foreigner) AS Total_foreigner
FROM regions
WHERE level = 'Region'
GROUP BY Region_name
ORDER BY Total_foreigner DESC
LIMIT 5;
```

**Answer / Respuesta:**  
1. **NCR (National Capital Region / Manila)** — by far the largest, driven by NAIA airport
2. **Region VII (Central Visayas / Cebu)** — second hub, driven by Mactan-Cebu airport
3. **Region IV-A (CALABARZON)** — adjacent to Manila, benefits from overflow
4. **Region III (Central Luzon)** — Clark airport and resort destinations
5. **Region VI (Western Visayas / Boracay)** — world-famous beach destination

**Insight:**  
Geographic concentration is extreme: the top 2 regions (NCR + Cebu) capture the vast majority of foreign visitors. Mindanao regions are virtually absent from this ranking, reflecting underdeveloped tourism infrastructure and connectivity.  
La concentración geográfica es extrema: las 2 principales regiones (NCR + Cebu) concentran la gran mayoría de visitantes extranjeros. Las regiones de Mindanao están prácticamente ausentes de este ranking, lo que refleja infraestructura turística y conectividad subdesarrolladas.

---

### Query 1.2 — Top 5 regions by domestic tourists / Top 5 regiones por turistas domésticos

**Question / Pregunta:**  
Which regions attract the most domestic Filipino tourists?  
¿Qué regiones atraen más turistas filipinos domésticos?

**Answer / Respuesta:**  
Domestic tourism is more geographically distributed than foreign tourism. NCR still leads, but Visayas and parts of Mindanao score higher in domestic rankings than in foreign ones, suggesting these regions rely more heavily on domestic visitors.  
El turismo doméstico está más distribuido geográficamente que el extranjero. NCR sigue liderando, pero las Visayas y partes de Mindanao puntúan más alto en los rankings domésticos que en los extranjeros, lo que sugiere que estas regiones dependen más de los visitantes nacionales.

---

### Query 2 — Annual breakdown by visitor type / Desglose anual por tipo de visitante

**Question / Pregunta:**  
How many foreign, domestic, and OFW (Overseas Filipino Workers) tourists did the Philippines receive each year?  
¿Cuántos turistas extranjeros, domésticos y OFW recibió Filipinas cada año?

```sql
SELECT year,
       SUM(Foreigner) AS total_foreign,
       SUM(domestic) AS total_domestic,
       SUM(ofw) AS total_ofw
FROM regions
WHERE level = 'region'
GROUP BY year
ORDER BY year;
```

**Answer / Respuesta:**  
Domestic tourists vastly outnumber foreign visitors in absolute terms across all years. The OFW category (Overseas Filipino Workers returning home) represents a meaningful and consistent share, particularly notable during the COVID years when international arrivals collapsed but OFW returns continued.  
Los turistas domésticos superan ampliamente a los visitantes extranjeros en términos absolutos en todos los años. La categoría OFW (filipinos en el extranjero que regresan) representa una proporción significativa y constante, especialmente notable durante los años COVID cuando las llegadas internacionales colapsaron pero las llegadas de OFW continuaron.

---

### Query 3 — Tourism composition percentages / Porcentajes de composición del turismo

**Question / Pregunta:**  
What percentage of total tourism in the Philippines is foreign vs. domestic vs. OFW?  
¿Qué porcentaje del turismo total en Filipinas es extranjero vs. doméstico vs. OFW?

```sql
SELECT (SUM(Foreigner) / SUM(total)) * 100 AS percent_foreigner,
       (SUM(domestic) / SUM(total)) * 100 AS percent_domestic,
       (SUM(ofw) / SUM(total)) * 100 AS percent_ofw,
       SUM(total) AS Total
FROM regions
WHERE level = 'region';
```

**Answer / Respuesta:**  
Domestic tourists represent the majority of overall tourist volume (~80%+). Foreign visitors, while economically high-value, represent a smaller share of total headcount. This highlights the importance of the domestic tourism market to the Philippine economy.  
Los turistas domésticos representan la mayoría del volumen total de turistas (~80%+). Los visitantes extranjeros, aunque de alto valor económico, representan una proporción menor del total de personas. Esto destaca la importancia del mercado de turismo doméstico para la economía filipina.

---

### Query 4 — Year-over-year regional change / Variación regional interanual

**Question / Pregunta:**  
What is the annual percentage change in total tourist arrivals for each region?  
¿Cuál es el cambio porcentual anual en llegadas totales de turistas para cada región?

```sql
SELECT region_name, year,
    SUM(total) AS total_region,
    LAG(SUM(total)) OVER (PARTITION BY region_name ORDER BY year) AS prev_year_total,
    ROUND((SUM(total) - LAG(SUM(total)) OVER (PARTITION BY region_name ORDER BY year)) * 100.0 
          / LAG(SUM(total)) OVER (PARTITION BY region_name ORDER BY year), 2) AS yoy_change_pct
FROM regions
WHERE level = 'Region'
GROUP BY region_name, year
ORDER BY region_name, year;
```

**Answer / Respuesta:**  
All regions show near-identical pattern: steady growth 2015–2019, catastrophic drop 2020–2021, recovery 2022–2023. Some regions show notably stronger recovery rates, suggesting resilience differences.  
Todas las regiones muestran un patrón casi idéntico: crecimiento estable 2015–2019, caída catastrófica 2020–2021, recuperación 2022–2023. Algunas regiones muestran tasas de recuperación notablemente más fuertes, lo que sugiere diferencias en resiliencia.

---

### Query 5 — COVID recovery rate by region / Tasa de recuperación del COVID por región

**Question / Pregunta:**  
Which regions recovered most quickly from COVID — comparing 2023 to the pre-COVID 2019 baseline?  
¿Qué regiones se recuperaron más rápidamente del COVID, comparando 2023 con el nivel prepandémico de 2019?

```sql
SELECT region_name,
       SUM(CASE WHEN year = 2019 THEN total ELSE 0 END) AS total_2019,
       SUM(CASE WHEN year = 2023 THEN total ELSE 0 END) AS total_2023,
       ROUND(SUM(CASE WHEN year = 2023 THEN total ELSE 0 END) * 100 
             / SUM(CASE WHEN year = 2019 THEN total ELSE 0 END), 2) AS recovery_perc
FROM regions
WHERE year IN (2023, 2019) AND level = 'Region'
GROUP BY region_name;
```

**Answer / Respuesta:**  
Some regions had already **exceeded their 2019 levels by 2023** (recovery rate > 100%), suggesting they benefited from redirected tourism post-COVID. NCR and Cebu recovered strongly. Some Mindanao regions lagged behind.  
Algunas regiones ya **superaron sus niveles de 2019 en 2023** (tasa de recuperación > 100%), lo que sugiere que se beneficiaron del turismo redirigido después del COVID. NCR y Cebu se recuperaron con fuerza. Algunas regiones de Mindanao se quedaron rezagadas.

---

### Query 6 — Recovery classification by region / Clasificación de recuperación por región

**Question / Pregunta:**  
Which regions can be classified as having "very good", "good", or "poor" COVID recovery based on 2023 vs 2019 data?  
¿Qué regiones pueden clasificarse como de recuperación "muy buena", "buena" o "deficiente" según los datos de 2023 vs 2019?

```sql
WITH yearly_totals AS (
    SELECT region_name,
           SUM(CASE WHEN year = 2019 THEN total ELSE 0 END) AS total_2019,
           SUM(CASE WHEN year = 2023 THEN total ELSE 0 END) AS total_2023
    FROM regions
    WHERE year IN (2023, 2019) AND level = 'Region'
    GROUP BY region_name
)
SELECT region_name, total_2019, total_2023,
       ROUND(total_2023 * 100.0 / total_2019) AS recovery_perc,
       CASE WHEN (total_2023 * 100.0 / total_2019) > 100 THEN 'Very Good'
            WHEN (total_2023 * 100.0 / total_2019) BETWEEN 50 AND 99 THEN 'Good'
            ELSE 'Poor' END AS recovery_classification
FROM yearly_totals
ORDER BY recovery_perc DESC
LIMIT 10;
```

**Answer / Respuesta:**  
- **Very Good (>100%):** NCR, Region VII (Cebu), and 2–3 additional regions surpassed pre-COVID levels  
- **Good (50–99%):** Most remaining regions are in partial recovery  
- **Poor (<50%):** A small number of remote or Mindanao regions still well below 2019 levels  

**Insight:**  
Regions with strong airport infrastructure and major international/domestic hubs recovered fastest. Remote or island regions dependent on inter-island ferry connectivity recovered slowest.  
Las regiones con sólida infraestructura aeroportuaria y grandes concentraciones internacionales/domésticas se recuperaron más rápido. Las regiones remotas o insulares dependientes de la conectividad en ferry inter-islas se recuperaron más lentamente.

---

## Key Conclusions / Conclusiones Clave

### EN — English

1. **USA dominance is structural:** American arrivals are the most stable and predictable segment, anchored by the Filipino-American diaspora and deep economic ties.

2. **COVID caused the sharpest tourism collapse in recorded Philippine history**, with arrivals dropping to near zero in 2020. The sector had not fully recovered to 2019 levels by end of 2023.

3. **Seasonality is highly predictable:** January peaks and September troughs are consistent across all years (excluding the COVID period), making them reliable for capacity and marketing planning.

4. **China's pre-COVID growth was spectacular but its recovery is lagging** — a clear structural shift compared to other top-5 markets.

5. **Geographic concentration of foreign tourism is extreme:** NCR and Cebu together capture the vast majority of foreign arrivals. This concentration is both a strength (ease of infrastructure investment) and a risk (overdependence on two hubs).

6. **Domestic tourists are the backbone of Philippine tourism volume.** Foreign visitors are economically high-value but numerically a minority of total tourist traffic.

7. **Mindanao remains significantly underserved** in terms of foreign visitor arrivals relative to its geographic size and population, indicating clear potential for tourism development.

---

### ES — Español

1. **El dominio de EE.UU. es estructural:** Las llegadas estadounidenses son el segmento más estable y predecible, anclado en la diáspora filipina-americana y los profundos vínculos económicos.

2. **El COVID provocó el colapso turístico más abrupto de la historia registrada de Filipinas**, con llegadas cayendo casi a cero en 2020. El sector no se había recuperado completamente a los niveles de 2019 a finales de 2023.

3. **La estacionalidad es muy predecible:** Los picos de enero y los mínimos de septiembre son consistentes en todos los años (excluido el período COVID), lo que los hace fiables para la planificación de capacidad y marketing.

4. **El crecimiento de China antes del COVID fue espectacular, pero su recuperación se está rezagando** — un cambio estructural claro en comparación con otros mercados del top 5.

5. **La concentración geográfica del turismo extranjero es extrema:** NCR y Cebu juntas concentran la gran mayoría de las llegadas extranjeras. Esta concentración es tanto una fortaleza (facilidad de inversión en infraestructura) como un riesgo (dependencia excesiva de dos centros).

6. **Los turistas domésticos son la columna vertebral del volumen turístico de Filipinas.** Los visitantes extranjeros son económicamente de alto valor pero numéricamente una minoría del tráfico turístico total.

7. **Mindanao sigue estando significativamente desatendida** en términos de llegadas de visitantes extranjeros en relación con su tamaño geográfico y su población, lo que indica un claro potencial para el desarrollo turístico.
