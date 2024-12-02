-- 2 exercise




DROP TABLE test_numeric;

CREATE TABLE IF NOT EXISTS test_numeric
( measurement numeric,
description text
);


INSERT INTO test_numeric
VALUES ( 1234567890.0987654321,
'Точность 20 знаков, масштаб 10 знаков' );
INSERT INTO test_numeric
VALUES ( 1.5,
'Точность 2 знака, масштаб 1 знак' );
INSERT INTO test_numeric
VALUES ( 0.12345678901234567890,
'Точность 21 знак, масштаб 20 знаков' );
INSERT INTO test_numeric
VALUES ( 1234567890,
'Точность 10 знаков, масштаб 0 знаков (целое число)');


SELECT *
FROM test_numeric

SELECT '5e-324'::double precision > '4e-324'::double precision;

SELECT '5e-324'::double precision;
SELECT '4e-324'::double precision;

-- 4 exercise
-- real 1e-37 1e+37
SELECT '1E-37'::REAL < '1E-36'::REAL;
SELECT '1E+37'::REAL > '1E+36'::REAL;

-- double 1E-307 до 1E+308
SELECT '1E-307'::DOUBLE PRECISION < '1E-306'::DOUBLE PRECISION;
SELECT '1E+307'::DOUBLE PRECISION > '1E+306'::DOUBLE PRECISION;


-- 8 exercise

CREATE TABLE test_serial
(   id serial PRIMARY KEY,
    name text
);

INSERT INTO test_serial ( name ) VALUES ( 'Вишневая' );
INSERT INTO test_serial ( id, name ) VALUES ( 2, 'Прохладная' );

INSERT INTO test_serial ( name ) VALUES ( 'Грушевая' );


-- 12 exercise
SHOW datestyle;

SET datestyle TO 'MDY';

SELECT '18-05-2016'::date;

SELECT '05-18-2016'::date;


SET datestyle TO DEFAULT;

SET datestyle TO 'Postgres, DMY';


SET datestyle TO 'SQL, DMY';

SET datestyle TO 'German, DMY';


--15
SELECT FORMAT('%s-%s-%s', TO_CHAR(now(), 'dd'), TO_CHAR(now(), 'MM'), TO_CHAR(now(), 'YY'));    

--21 
SELECT ( '2016-01-31'::date + '1 mon'::interval ) AS new_date;




SELECT ( '2016-02-29'::date + '1 mon'::interval + '1 day'::interval) AS new_date;

SELECT ( '2016-02-29'::date + '1 mon'::interval ) AS new_date;


SELECT ( '2016-01-01'::date + '1 mon'::interval) AS new_date;

SELECT DATE_TRUNC('month', now()) +  INTERVAL '1 month' - INTERVAL '1 day'

--30
CREATE TABLE test_bool
(   a boolean,
    b text
);
SELECT * FROM test_bool;

INSERT INTO test_bool VALUES ( TRUE, 'yes' ); -- t
INSERT INTO test_bool VALUES ( yes, 'yes' ); -- f
INSERT INTO test_bool VALUES ( 'yes', true ); -- t
INSERT INTO test_bool VALUES ( 'yes', TRUE ); -- t
INSERT INTO test_bool VALUES ( '1', 'true' ); --t
INSERT INTO test_bool VALUES ( 1, 'true' ); --f
INSERT INTO test_bool VALUES ( 't', 'true' ); --t
INSERT INTO test_bool VALUES ( 't', truth ); --f
INSERT INTO test_bool VALUES ( true, true ); --t
INSERT INTO test_bool VALUES ( 1::boolean, 'true' ); --t
INSERT INTO test_bool VALUES ( 111::boolean, 'true' );--t



--33
DROP TABLE pilots;
CREATE TABLE pilots
( pilot_name text,
    schedule integer[],
    meal text[]
);

INSERT INTO pilots
VALUES ( 'Ivan', '{ 1, 3, 5, 6, 7 }'::integer[],
'{ "сосиска", "макароны", "кофе" }'::text[]
),
( 'Petr', '{ 1, 2, 5, 7 }'::integer [],
'{ "котлета", "каша", "кофе" }'::text[]
),
( 'Pavel', '{ 2, 5 }'::integer[],
'{ "сосиска", "каша", "кофе" }'::text[]
),
( 'Boris', '{ 3, 5, 6 }'::integer[],
'{ "котлета", "каша", "чай" }'::text[]
);

SELECT * FROM pilots;

UPDATE pilots
SET meal = '{ { "сосиска", "макароны", "кофе" },
                { "котлета", "каша", "кофе" },
                { "сосиска", "каша", "кофе" },
                { "котлета", "каша", "чай" } }'::text[][]
WHERE pilot_name IN ('Ivan', 'Pavel');

UPDATE pilots
SET meal = '{ { "сосиска", "каша", "кофе" },
                { "котлета", "каша", "кофе" },
                { "котлета", "каша", "чай" },
                { "котлета", "каша", "чай" } }'::text[][]
WHERE pilot_name IN ('Boris', 'Petr');

SELECT '{"topic": "load_src", "message":{"status": 1, "errors": 0}}'::JSONB || '{"headers": "kafka_isnt_set"}'::JSONB;



--35
