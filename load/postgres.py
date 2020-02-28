import pandas as pd

from connection.postgres_config import create_engine_config, dispose_engine, check_schema_exist


# TODO: Drop all table in postgres (WH)

# Read from db and set it as data frame
def select_table(sql_query, schema, db_properties):
    try:
        engine = create_engine_config(schema, db_properties)
        if engine is not None:
            table = pd.read_sql_query(sql_query, engine)
            return table
    except:
        return ''


# To insert to database
def upsert_table(data_frame, schema, table_name, db_properties):
    engine = create_engine_config(schema, db_properties)
    if engine is not None:
        data_frame.to_sql(table_name, con=engine, if_exists='replace')

        # Try to close connection
        dispose_engine(engine)


def test_retrieve_postgres(db_properties):
    check_schema_exist("wekan", db_properties)
