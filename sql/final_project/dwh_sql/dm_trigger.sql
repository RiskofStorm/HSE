CREATE OR REPLACE FUNCTION core.write_dm_metadata(schema_name text, table_name text)
RETURNS void AS
$$
DECLARE
    v_cnt bigint;
BEGIN 
    EXECUTE FORMAT('REFRESH MATERIALIZED VIEW %I.%I ;', schema_name, table_name);
    EXECUTE FORMAT('SELECT COUNT(*) FROM %I.%I;', schema_name, table_name) INTO v_cnt;
    EXECUTE FORMAT('INSERT INTO core.datamart_metadata(schema_name, table_name, load_dt, cnt_rows)
                    VALUES(''%s'',
                           ''%s'',
                           CURRENT_TIMESTAMP,
                           ''%s''
                    );
    ', schema_name, table_name, v_cnt);
    
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION core.write_dm_metadata_cdm_stocks_stats_monthly()
RETURNS trigger AS
$$
BEGIN
    EXECUTE core.write_dm_metadata('cdm', 'stocks_stats_monthly');
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS trigger_fn_dds_ticker ON dds.ticker_price_history;
CREATE TRIGGER trigger_fn_dds_ticker
    AFTER INSERT
    ON dds.ticker_price_history
    FOR EACH STATEMENT
    EXECUTE FUNCTION core.write_dm_metadata_cdm_stocks_stats_monthly();
