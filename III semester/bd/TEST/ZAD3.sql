-- Patrycja Ziemkiewicz 459640 gr 2, ORACLE, zadanie 3
WITH 
sub AS(
    SELECT name AS buyer, COALESCE(price, 0) AS price,  ROW_NUMBER() OVER (PARTITION BY name ORDER BY price DESC) AS rank 
    FROM Sales 
    RIGHT JOIN Company c ON c.name = Sales.buyer
)
SELECT buyer
FROM sub 
GROUP BY buyer
HAVING SUM(price) * 0.9 <= SUM(CASE WHEN rank <= 3 THEN price ELSE 0 END)
ORDER BY buyer;