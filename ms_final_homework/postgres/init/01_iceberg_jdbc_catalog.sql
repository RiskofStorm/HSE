CREATE TABLE IF NOT EXISTS iceberg_tables (
    catalog_name VARCHAR NOT NULL,
    table_namespace VARCHAR NOT NULL,
    table_name VARCHAR NOT NULL,
    metadata_location VARCHAR,
    previous_metadata_location VARCHAR,
    PRIMARY KEY (catalog_name, table_namespace, table_name)
);

CREATE TABLE IF NOT EXISTS iceberg_namespaces (
    catalog_name VARCHAR NOT NULL,
    namespace VARCHAR NOT NULL,
    PRIMARY KEY (catalog_name, namespace)
);

CREATE TABLE IF NOT EXISTS iceberg_namespace_properties (
    catalog_name VARCHAR NOT NULL,
    namespace VARCHAR NOT NULL,
    property_key VARCHAR NOT NULL,
    property_value VARCHAR,
    PRIMARY KEY (catalog_name, namespace, property_key)
);
