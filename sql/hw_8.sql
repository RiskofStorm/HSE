--CREATE TEMP TABLE aircrafts_tmp AS
--SELECT * FROM aircrafts WITH NO DATA;
--
--ALTER TABLE aircrafts_tmp
--ADD PRIMARY KEY ( aircraft_code );
--ALTER TABLE aircrafts_tmp
--ADD UNIQUE ( model );
DROP TABLE aircrafts_tmp;
CREATE  TABLE aircrafts_tmp
( LIKE aircrafts INCLUDING CONSTRAINTS INCLUDING INDEXES );


INSERT INTO aircrafts_tmp
SELECT * FROM aircrafts;

COMMIT;
ROLLBACK;



-- 2.1
BEGIN;
    
SELECT *
FROM aircrafts_tmp
WHERE range < 2000;

UPDATE aircrafts_tmp
SET range = 2100
WHERE aircraft_code = 'CN1';

UPDATE aircrafts_tmp
SET range = 1900
WHERE aircraft_code = 'CR2';

ROLLBACK;



--3.1
BEGIN;

UPDATE aircrafts_tmp
SET range = 2100
WHERE aircraft_code = 'CR2';
COMMIT;

SELECT  pg_current_logfile();
SHOW logging_collector;
SHOW log_directory;

SELECT *
FROM aircrafts_tmp at2 

-- ДЗ 9


-- 3 



-- 6

-- 8