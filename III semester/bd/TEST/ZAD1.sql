-- Patrycja Ziemkiewicz 459640 gr 2, ORACLE, zadanie 1
WITH 
s AS (SELECT seller, SUM(price) as sold FROM Sales GROUP BY seller),
b as (SELECT buyer, SUM(-price) as bought FROM Sales GROUP BY buyer)
select name, COALESCE(sold + bought, 0) AS bilans 
FROM Company c
LEFT JOIN s ON s.seller = c.name
LEFT JOIN b ON b.buyer = c.name
ORDER BY bilans DESC;