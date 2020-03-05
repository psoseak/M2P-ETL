from src.connection.postgres_connection import dispose_engine
from src.util.message import *


class PostgresLoad:
    def __init__(self, postgres_connection):
        self.postgres_connection = postgres_connection

    # To insert to database
    def upsert_table(self, data_frame, table_name):
        engine = self.postgres_connection.create_engine_config()
        if engine is not None:
            data_frame.to_sql(table_name, con=engine, if_exists='replace')

            # Try to close connection
            dispose_engine(engine)

    def check_schema_exist(self):
        engine = self.postgres_connection.create_engine_config()
        if engine is not None:
            # Read
            sql_query = "SELECT COUNT(schema_name) FROM information_schema.schemata " \
                        "WHERE schema_name = '{}'"\
                        .format(self.postgres_connection.get_db_properties().schema)
            result = engine.execute(sql_query).scalar()
            if result == 0:
                # schema does not exist
                # create schema
                sql_query = "CREATE SCHEMA IF NOT EXISTS {}"\
                            .format(self.postgres_connection.get_db_properties().schema)
                engine.execute(sql_query)
                warning_no_schema(self.postgres_connection.get_db_properties())

    # delete all table
    def delete_all_by_schema(self):
        engine = self.postgres_connection.create_engine_config()

        if engine is not None:
            sql_query = "SELECT COUNT(schema_name) FROM information_schema.schemata " \
                        "WHERE schema_name = '{}'"\
                        .format(self.postgres_connection.get_db_properties().schema)

            result = engine.execute(sql_query).scalar()

            if result == 1:
                sql_query = 'DROP SCHEMA {schema} CASCADE'.format(
                    schema=self.postgres_connection.get_db_properties().schema
                )
                engine.execute(sql_query)
