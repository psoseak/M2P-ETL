import pandas as pd
import util as log

from connection.postgres_connection import create_engine_config, dispose_engine


# Read from db and set it as data frame
def select_table(sql_query, db_properties):
    try:
        engine = create_engine_config(db_properties)
        if engine is not None:
            table = pd.read_sql_query(sql_query, engine)
            return table
    except:
        return ''


# To insert to database
def upsert_table(data_frame, table_name, db_properties):
    engine = create_engine_config(db_properties)
    if engine is not None:
        data_frame.to_sql(table_name, con=engine, if_exists='replace')

        # Try to close connection
        dispose_engine(engine)


def check_schema_exist(db_properties):
    engine = create_engine_config(db_properties)
    if engine is not None:
        # Read
        sql_query = "SELECT COUNT(schema_name) FROM information_schema.schemata WHERE schema_name = '{}'".format(
            db_properties.schema)
        result = engine.execute(sql_query).scalar()
        if result == 0:
            # schema does not exist
            # create schema
            sql_query = "CREATE SCHEMA IF NOT EXISTS {}".format(db_properties.schema)
            engine.execute(sql_query)
            log.message.warning_no_schema(db_properties)


# delete all table
def delete_all_by_schema(db_properties):
    engine = create_engine_config(db_properties)

    if engine is not None:
        sql_query = "SELECT COUNT(schema_name) FROM information_schema.schemata WHERE schema_name = '{}'".format(
            db_properties.schema)

        result = engine.execute(sql_query).scalar()

        if result == 1:
            sql_query = 'DROP SCHEMA {schema} CASCADE'.format(
                schema=db_properties.schema
            )
            engine.execute(sql_query)
