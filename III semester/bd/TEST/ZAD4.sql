-- Patrycja Ziemkiewicz 459640 gr 2, ORACLE, zadanie 4
WITH 
sub AS (SELECT buyer, price, id, ROW_NUMBER() OVER (PARTITION BY buyer ORDER BY id) AS rank FROM Sales)
SELECT s.buyer, COUNT(*) AS count
FROM sub s, sub d
WHERE s.buyer = d.buyer AND s.price >= 2 * d.price AND s.rank = d.rank - 1
GROUP BY s.buyer
ORDER BY count DESC;
