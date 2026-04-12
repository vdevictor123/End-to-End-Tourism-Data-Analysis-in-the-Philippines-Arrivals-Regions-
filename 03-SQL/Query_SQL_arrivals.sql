SELECT * FROM philippine.arrivals;

#1 Top 1 en total que ha vistiado filipinas
select country_of_residence,
		sum(jan_dec) as total
from arrivals 
group by country_of_residence
order by total desc
limit 1;

#2 Top 10 country residence total de los años 2015-2023
Select country_of_residence,
		sum(jan_dec)as total
from arrivals
group by country_of_residence
order by total desc
limit 10;

#3- Top 1 de pais origen de tursitas por año
Select country_of_residence,
       YEAR,
       total       
from ( Select country_of_residence,
			  year,
              sum(jan_dec) as total,
              row_number() over(partition by year order by sum(jan_dec) desc) as rn
	   from arrivals
	   group by country_of_residence, year) t
where rn <= 1;

#4 Cual es el promedio de turistas por pais durante estos años 2015-2023
SELECT country_of_residence,
       ROUND(AVG(total_anual)) AS promedio_anual
FROM (
    SELECT country_of_residence,
           year,
           SUM(jan_dec) AS total_anual
    FROM arrivals
    GROUP BY country_of_residence, year
) t
GROUP BY country_of_residence
ORDER BY promedio_anual DESC;

# 5 Evolucion arrivals de España por mes y año.
Select *
From arrivals
where country_of_residence = "Spain";

# 6 Crecimiento de visitas a PH durante los años(2015-2023) de Spain
Select country_of_residence,
	jan_dec,
    year,
    LAG(jan_dec) OVER(Order by year) as pre_year,
    ROUND((jan_dec - LAG(jan_dec) OVER(order by year)) * 100 / LAG(jan_dec) over(order by year)) as Percent
from arrivals
where country_of_residence = "Spain";

# 6 Crecimiento de visitas a PH durante los años(2015-2023) de "USA"
Select country_of_residence,
	jan_dec,
	year,
    Lag(jan_dec) over(order by year) as pre_year,
    Round((jan_dec - lag(jan_dec)over(order by year))*100 / lag(jan_dec) over(order by year)) as percent
from arrivals
where country_of_residence = "USA";
    
# 7 Crecimiento de visitas a PH durante los años(2015-2023) de "CHINA"
Select country_of_residence,
		year,
        jan_dec,
        lag(jan_dec) over(order by year) as pre_year,
        Round((jan_dec - lag(jan_dec) over(order by year))*100 / lag(jan_dec) over(order by year)) as percent
From arrivals
where country_of_residence = "China";
        
# 8 Compara el % entre "USA" y "China" por año
Select country_of_residence,
	jan_dec,
	year,
    lag(jan_dec) over(PARTITION by country_of_residence order by year) as pre_year,
    round((jan_dec - lag(jan_dec) over(Partition by country_of_residence order by year))*100 / lag(jan_dec) over(partition by country_of_residence order by year),2) as percent
From arrivals
where country_of_residence in ("USA","China")
order by year;
 
 
#9 Ranking de meses por total de turistas llegados a Filipinas (2015-2023)
-- Suma todos los países y todos los años por mes
SELECT 'January' AS month, SUM(january) AS total_tourist FROM arrivals
UNION ALL
SELECT 'February', SUM(february) FROM arrivals
UNION ALL
SELECT 'March', SUM(march) FROM arrivals
UNION ALL
SELECT 'April', SUM(april) FROM arrivals
UNION ALL
SELECT 'May', SUM(may) FROM arrivals
UNION ALL
SELECT 'June', SUM(june) FROM arrivals
UNION ALL
SELECT 'July', SUM(july) FROM arrivals
UNION ALL
SELECT 'August', SUM(august) FROM arrivals
UNION ALL
SELECT 'September', SUM(september) FROM arrivals
UNION ALL
SELECT 'October', SUM(october) FROM arrivals
UNION ALL
SELECT 'November', SUM(november) FROM arrivals
UNION ALL
SELECT 'December', SUM(december) FROM arrivals
ORDER BY total_tourist DESC;









	
