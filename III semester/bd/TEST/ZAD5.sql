-- Patrycja Ziemkiewicz 459640 gr 2, ORACLE, zadanie 5
WITH zal(co, od) AS (
    SELECT name, name FROM Company
    UNION ALL 
    SELECT company, od FROM zal JOIN Ownership o ON zal.co = o.shareholder
), 
sub AS (
    SELECT SUM(price) as wewnetrzne
    FROM Sales
    LEFT JOIN zal z1 ON z1.co = Sales.buyer
    LEFT JOIN zal z2 ON z2.od = Sales.buyer
    WHERE seller = z1.od OR seller = z2.co
),
w AS (
    SELECT SUM(price) AS wszystkie
    FROM Sales
)
SELECT wewnetrzne / wszystkie AS procent
FROM w, sub;