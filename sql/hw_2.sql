CREATE TABLE bookings.aircrafts(  
    aircraft_code char( 3 ) NOT NULL,
    model text NOT NULL,
    range integer NOT NULL,
    CHECK ( range > 0 ),
    PRIMARY KEY ( aircraft_code )
);


SELECT
    *
FROM
    aircrafts_data;



INSERT into aircrafts_data
VALUES ( 'SU9', '{"model":"Sukhoi SuperJet-100"}'::JSON, 3000 );




UPDATE aircrafts_data
SET range= RANGE*2
WHERE model = '{"en": "Sukhoi Superjet-100", "ru": "Сухой Суперджет-100"}'::JSONB;

SELECT *
FROM aircrafts ;


DELETE FROM aircrafts_data
WHERE aircraft_code = 'LLM'


SELECT
    *
FROM
    aircrafts
ORDER BY
    range DESC