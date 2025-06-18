CREATE OR REPLACE FUNCTION export_tableinfo2excel(table_name text, schema_name text, output_file_path text)
RETURNS void AS $$
import pandas as pd
import openpyxl as xl
from openpyxl.utils.dataframe import dataframe_to_rows

def execute_query(query):
    plan = plpy.prepare(query)
    return plpy.execute(plan)

comment_on_table_query = f"""
SELECT obj_description((SELECT oid FROM pg_class where relname = '{table_name}' LIMIT 1))
FROM pg_class
WHERE relkind = 'r'
LIMIT 1
"""
table_full_column_data_query = f"""
SELECT
    t1.table_catalog AS db_name
    ,t1.table_schema 
    ,t1.column_name
    ,t2.description
    ,t1.column_default 
    ,t1.is_nullable
    ,t1.data_type
    ,t1.udt_name
    ,t1.character_maximum_length
    ,t1.character_octet_length 
    ,t1.numeric_precision 
    ,t1.numeric_scale
    ,t1.datetime_precision
    ,t1.is_generated
FROM information_schema.columns t1
INNER JOIN(
    SELECT
        c.table_schema,
        c.table_name,
        c.column_name,
        pgd.description
    FROM pg_catalog.pg_statio_all_tables AS st
    INNER JOIN pg_catalog.pg_description pgd 
        ON pgd.objoid = st.relid
    INNER JOIN information_schema.columns c 
        ON  pgd.objsubid   = c.ordinal_position 
        AND c.table_schema = st.schemaname
        AND c.table_name   = st.relname
    WHERE table_schema = '{schema_name}'
        AND table_name = '{table_name}'
)t2
    ON t1.table_name = t2.table_name 
        AND t1.table_schema = t2.table_schema
        AND t1.column_name  = t2.column_name
ORDER BY ordinal_position
"""

table_indexes_query = f"""
select 
    c.relnamespace::regnamespace as schema_name,
    c.relname as table_name,
    i.indexrelid::regclass as index_name,
    i.indisprimary as is_pk,
    i.indisunique as is_unique
from pg_index i
join pg_class c on c.oid = i.indrelid
where c.relname = '{table_name}'
"""

excel_wb = xl.Workbook()

table_info = excel_wb.create_sheet("table_info")
table_info_headers = [
    'db_name',
    'table_schema',
    'column_name',
    'description',
    'column_default',
    'is_nullable',
    'data_type',
    'udt_name',
    'character_maximum_length',
    'character_octet_length', 
    'numeric_precision', 
    'numeric_scale',
    'datetime_precision',
    'is_generated'
]

table_indexes = excel_wb.create_sheet("table_indexes")
table_indexes_headers = [
    'schema_name',
    'table_name',
    'index_name',
    'is_pk',
    'is_unique'
]

table_misc =  excel_wb.create_sheet("table_misc")
table_misc_headers = [
    'table_description'
]

queries = [
    table_full_column_data_query, 
    table_indexes_query,
    comment_on_table_query
]

headers = [
  table_info_headers,
  table_indexes_headers,
  table_misc_headers

]

excel_sheets = [
    table_info,
    table_indexes,
    table_misc
]


for query, excel_sheet, columns_names in zip(queries, excel_sheets, headers):

    res = execute_query(query)
    temp_data = tuple(tuple(i.values()) for i in res)
    df = pd.DataFrame.from_records(temp_data,columns=columns_names)
    for row in dataframe_to_rows(df, index=False, header=True):
        excel_sheet.append(row)


excel_wb.save(f'{output_file_path}/{table_name}.xlsx')

$$ LANGUAGE plpython3u VOLATILE SECURITY DEFINER;