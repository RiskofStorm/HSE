
-- INSERTS HUBS

INSERT INTO student1.hub_customer_location (
    location_hashkey, city, state, postal_code, region, load_date, record_source
)
SELECT DISTINCT
    MD5(CONCAT(city, '|', state, '|', postal_code, '|', region)) as location_hashkey,
    city, state, postal_code, region,
    CURRENT_TIMESTAMP, 'stg_superstore_sales'
FROM student1.stg_superstore_sales s
WHERE NOT EXISTS (
    SELECT 1 FROM student1.hub_customer_location h
    WHERE h.location_hashkey = MD5(CONCAT(s.city, '|', s.state, '|', s.postal_code, '|', s.region))
);

INSERT INTO student1.hub_product (
    product_hashkey, category, sub_category, load_date, record_source
)
SELECT DISTINCT
    MD5(CONCAT(category, '|', sub_category)),
    category, 
    sub_category, 
    CURRENT_TIMESTAMP, 
    'stg_superstore_sales'
FROM student1.stg_superstore_sales s
WHERE NOT EXISTS (
    SELECT 1 FROM student1.hub_product h
    WHERE h.product_hashkey = MD5(CONCAT(s.category, '|', s.sub_category))
);

INSERT INTO student1.hub_customer_segment (
    segment_hashkey, segment, load_date, record_source
)
SELECT DISTINCT 
	   MD5(segment), 
	   segment, 
	   CURRENT_TIMESTAMP, 
	   'stg_superstore_sales'
FROM student1.stg_superstore_sales s
WHERE NOT EXISTS (
    SELECT 1 FROM student1.hub_customer_segment h
    WHERE h.segment_hashkey = MD5(s.segment)
);


INSERT INTO student1.hub_shipping_method (
    shipping_hashkey, 
    ship_mode, 
    load_date, 
    record_source
)
SELECT DISTINCT
    MD5(ship_mode), 
    ship_mode, 
    CURRENT_TIMESTAMP, 
    'stg_superstore_sales'
FROM student1.stg_superstore_sales s
WHERE NOT EXISTS (
    SELECT 1 FROM student1.hub_shipping_method h
    WHERE h.shipping_hashkey = MD5(s.ship_mode)
);

-- STEP 3: Link Table
INSERT INTO student1.link_sales_transaction (
    sales_transaction_hashkey, location_hashkey, product_hashkey,
    segment_hashkey, shipping_hashkey, load_date, record_source
)
SELECT DISTINCT
    MD5(CONCAT(
        MD5(CONCAT(s.city, '|', s.state, '|', s.postal_code, '|', s.region)), '|',
        MD5(CONCAT(s.category, '|', s.sub_category)), '|',
        MD5(s.segment), '|', MD5(s.ship_mode), '|',
        ROW_NUMBER() OVER (ORDER BY s.load_date, s.city)
    )) as sales_transaction_hashkey,
    MD5(CONCAT(s.city, '|', s.state, '|', s.postal_code, '|', s.region)),
    MD5(CONCAT(s.category, '|', s.sub_category)),
    MD5(s.segment),
    MD5(s.ship_mode),
    s.load_date, s.record_source
FROM student1.stg_superstore_sales s;

-- STEP 4: Satellites
INSERT INTO student1.sat_customer_location (
    location_hashkey, load_date, load_end_date, country, is_current, record_source
)
SELECT distinct MD5(CONCAT(s.city, '|', s.state, '|', s.postal_code, '|', s.region)),
    s.load_date, null::timestamp ESTAMP, s.country, TRUE, s.record_source
FROM student1.stg_superstore_sales s
WHERE NOT EXISTS (
    SELECT 1 FROM student1.sat_customer_location sat
    WHERE sat.location_hashkey = MD5(CONCAT(s.city, '|', s.state, '|', s.postal_code, '|', s.region))
    AND sat.is_current = TRUE
);

INSERT INTO student1.sat_sales_metrics (
    sales_transaction_hashkey, load_date, load_end_date, sales, quantity,
    discount, profit, is_current, record_source
)
SELECT 
    lt.sales_transaction_hashkey, s.load_date, NULL, s.sales, s.quantity,
    s.discount, s.profit, TRUE, s.record_source
FROM student1.stg_superstore_sales s
JOIN student1.link_sales_transaction lt 
    ON lt.location_hashkey = MD5(CONCAT(s.city, '|', s.state, '|', s.postal_code, '|', s.region))
    AND lt.product_hashkey = MD5(CONCAT(s.category, '|', s.sub_category))
    AND lt.segment_hashkey = MD5(s.segment)
    AND lt.shipping_hashkey = MD5(s.ship_mode);

--select count(*)
--FROM student1.stg_superstore_sales s
--JOIN student1.link_sales_transaction lt 
--    ON lt.location_hashkey = MD5(CONCAT(s.city, '|', s.state, '|', s.postal_code, '|', s.region))
--    AND lt.product_hashkey = MD5(CONCAT(s.category, '|', s.sub_category))
--    AND lt.segment_hashkey = MD5(s.segment)
--    AND lt.shipping_hashkey = MD5(s.ship_mode)
--group by lt.sales_transaction_hashkey, s.load_date
--having count(*)> 1


-- BUSINESS VAULT Point-in-Time table
INSERT INTO student1.bv_pit_sales_analysis (
    sales_transaction_hashkey, 
    snapshot_date, 
    location_hashkey,
    product_hashkey,
    segment_hashkey, 
    shipping_hashkey, 
    sales, 
    quantity, 
    discount, profit,
    profit_margin, 
    revenue_per_unit, 
    discount_amount
)
SELECT 
    lt.sales_transaction_hashkey, 
    CURRENT_DATE - interval '1 day' *(random() * 100000)::int, 
    lt.location_hashkey, 
    lt.product_hashkey,
    lt.segment_hashkey, 
    lt.shipping_hashkey, 
    sm.sales, 
    sm.quantity, 
    sm.discount, 
    sm.profit,
    CASE WHEN sm.sales > 0 THEN ROUND((sm.profit / sm.sales) * 100, 4) ELSE 0 END,
    CASE WHEN sm.quantity > 0 THEN ROUND(sm.sales / sm.quantity, 4) ELSE 0 END,
    ROUND(sm.sales * sm.discount, 4)
FROM student1.link_sales_transaction lt
JOIN student1.sat_sales_metrics sm ON lt.sales_transaction_hashkey = sm.sales_transaction_hashkey
WHERE sm.is_current = TRUE;

-- bridge table  
INSERT INTO student1.bridge_product_hierarchy (
    product_hashkey, category, sub_category, category_level, hierarchy_path, load_date, record_source
)
SELECT DISTINCT
    hp.product_hashkey, hp.category, hp.sub_category, 1,
    hp.category || ' > ' || hp.sub_category, CURRENT_TIMESTAMP, 'stg_superstore_sales'
FROM student1.hub_product hp;
