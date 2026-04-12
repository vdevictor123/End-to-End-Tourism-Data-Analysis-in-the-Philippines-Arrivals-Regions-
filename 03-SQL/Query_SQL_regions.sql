SELECT * FROM philippine.regions_master_clean;

-- 1. ¿Cuál es el top 5 de regiones con más turistas Foreigner totales acumulados en todo el periodo 2015-2023?
Select Region_name,
		Sum(Foreigner) as Total_foreinger
From regions
where level = "Region" #evitamos duplicados
group by Region_name
order by Total_foreinger desc
limit 5;

-- 1.2. ¿Cuál es el top 5 de regiones con más turistas Domestic totales acumulados en todo el periodo 2015-2023?
Select Region_name,		
		Sum(domestic) as Total_domestic
From regions
where level = "Region" #evitamos duplicados
group by Region_name
order by Total_domestic desc
limit 5;

-- 2. ¿Cuántos turistas extranjeros, domésticos y OFW recibió Filipinas en total cada año?
Select year,
		Sum(Foreigner) as total_foreinger,
		sum(domestic) as total_domestic,
		sum(ofw) as total_ofw
from regions
where level = "region" #evitamos duplicados
group by year
order by year;

-- 3. ¿Qué porcentaje del turismo total es extranjero vs doméstico a nivel nacional?
Select (Sum(Foreigner)/ sum(total))*100 as percent_foreigner,
	   (Sum(domestic)/ sum(total))*100 as percent_domestic,
       (Sum(ofw)/ sum(total))*100 as percent_ofw,
       Sum(total) as Total
From regions
where level = "region";
		
-- 4. ¿Cuál es la variación porcentual año a año (YoY) de turistas totales para cada región?
SELECT 
    region_name,
    year,
    SUM(total) AS total_region,
    LAG(
		SUM(total)) OVER (PARTITION BY region_name ORDER BY year) AS prev_year_total,
    ROUND(
		(SUM(total) - LAG(SUM(total)) OVER (PARTITION BY region_name ORDER BY year)) * 100.0 
		/ LAG(SUM(total)) OVER (PARTITION BY region_name ORDER BY year), 2) AS yoy_change_pct
FROM regions
WHERE level = 'Region'
GROUP BY region_name, year
ORDER BY region_name, year;

-- 5. ¿Qué región se recuperó más rápido del COVID, comparando 2023 vs 2019?
Select region_name,
       sum(case when year = 2019 then total else 0 end) as total_2019,
       sum(case when year = 2023 then total else 0 end) as total_2023,
       Round( sum(case when year = 2023 then total else 0 end) *100 / sum(case when year = 2019 then total else 0 end), 2 ) as recovery_perc 
From regions
where year in (2023,2019) and level = 'Region'
group by region_name;

-- 6. Top 10 regiones con más turistas extranjeros en 2023
       
with yartly_totals as (Select region_name,
       sum(case when year = 2019 then total else 0 end) as total_2019,
       sum(case when year = 2023 then total else 0 end) as total_2023      
	From regions
	where year in (2023,2019) and level = 'Region'
	group by region_name)
    
Select region_name,
		total_2019,
		total_2023,
        round(total_2023 * 100.0 / total_2019) as recovery_perc,
        case when (total_2023 * 100.0 / total_2019) > 100 then 'very good'
			 when (total_2023 * 100.0 / total_2019) between 50 and 99 then 'good'
			 else 'poor'  end as Recovery_classification
From yartly_totals
order by recovery_perc desc
limit 10;

