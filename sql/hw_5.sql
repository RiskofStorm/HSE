
--2
SELECT passenger_name
FROM tickets
WHERE passenger_name LIKE '_____ %';

--7
--SELECT * FROM aircrafts;
SELECT DISTINCT departure_city, arrival_city
FROM routes r
JOIN aircrafts a ON r.aircraft_code = a.aircraft_code
WHERE a.model = 'Боинг 777-300' AND departure_city > arrival_city
ORDER BY 1

--9
SELECT departure_city, arrival_city, count(*)
FROM routes
WHERE departure_city = 'Москва'
    AND arrival_city = 'Санкт-Петербург'
GROUP BY 1,2;

 --13
SELECT f.departure_city, f.arrival_city,
        max( tf.amount ), min( tf.amount )
FROM flights_v f
LEFT JOIN ticket_flights tf ON f.flight_id = tf.flight_id
GROUP BY 1, 2
HAVING min( tf.amount ) IS NULL
ORDER BY 1, 2;
 
 --19
 WITH RECURSIVE ranges ( min_sum, max_sum, level )
AS (
    VALUES( 0, 100000, 1 ),
    ( 100000, 200000, 1 ),
    ( 200000, 300000, 1 )
    
    UNION
    
    SELECT min_sum + 100000, max_sum + 100000, LEVEL + 1
    FROM ranges
    WHERE max_sum < ( SELECT max( total_amount ) FROM bookings )
)
SELECT * FROM ranges;

 --21
SELECT DISTINCT a.city
FROM airports a
WHERE NOT EXISTS (
                SELECT * FROM routes r
                WHERE r.departure_city = 'Москва'
                AND r.arrival_city = a.city
)
AND a.city <> 'Москва'
ORDER BY city;

SELECT city
FROM airports
WHERE city <> 'Москва'
EXCEPT
SELECT arrival_city
FROM routes
WHERE departure_city = 'Москва'
ORDER BY city;


 --23
WITH cte AS (SELECT DISTINCT city FROM airports)

SELECT count( * )
FROM cte AS a1
JOIN cte AS a2
ON a1.city <> a2.city;



