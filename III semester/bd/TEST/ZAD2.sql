-- Patrycja Ziemkiewicz 459640 gr 2, ORACLE, zadanie 2
WITH
sub AS(
    SELECT seller, COUNT(DISTINCT buyer) AS sold
    FROM Ownership o 
    JOIN Sales s ON o.company = s.seller
    WHERE buyer = shareholder
    GROUP BY seller
),
d AS (
    SELECT name, COUNT(shareholder) AS n_shareholders
    FROM Company c
    LEFT JOIN Ownership o ON c.name = o.company
    GROUP BY name
)
SELECT name
FROM d 
LEFT JOIN sub ON d.name = sub.seller
WHERE n_shareholders = 0 OR n_shareholders = sold
ORDER BY name;