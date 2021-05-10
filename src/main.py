import sys
import os
import pandas as pd
from connection.db_config import DbProperties
from connection.mongo_connection import MongoConnection
from connection.postgres_connection import PostgresConnection
from extract.mongo_extract import Extract
from load.postgres import PostgresLoad
from transform.mongo_postgres_transform import convert_dictionary_to_data_frame
import util as log


def run():
    # define the database properties
    log.message.info_start()
    db_properties_source = initialize_source()
    db_properties_destination = initialize_destination()

    postgres_connection = PostgresConnection(db_properties_destination)
    mongo_connection = MongoConnection(db_properties_source)
    database_status = pre_run_check(postgres_connection, mongo_connection)

    if database_status is True:
        extraction_instance = Extract(mongo_connection.get_client())
        wekan_data = extraction_instance.extract_data_from_database(db_properties_source.db)
        log.message.info_database_connected()

        # initialize postgres_connection
        postgres_load = PostgresLoad(postgres_connection)

        # pre-check for destination database
        postgres_load.delete_all_by_schema()
        postgres_load.check_schema_exist()
        for collection in wekan_data:
            if isinstance(wekan_data[collection], pd.DataFrame):
                postgres_load.upsert_table(wekan_data[collection], collection)
            else:
                # check for None collection, empty dicts values found in mongodb 
                if wekan_data[collection] is not None:
                    collection_data_frame = convert_dictionary_to_data_frame(
                        wekan_data[collection]).applymap(str)
                    if collection_data_frame.size > 0:
                        collection_data_frame = collection_data_frame.set_index("_id")

                    postgres_load.upsert_table(collection_data_frame, collection)
                else:
                    print(collection + "is None")

        log.message.info_migrated_completed()


def pre_run_check(postgres_connection, mongo_connection):
    postgres_status = postgres_connection.check_connection()
    mongo_status = mongo_connection.check_connection()
    postgres_connection.check_database_exist()
    if postgres_status and mongo_status:
        return True
    else:
        if not mongo_status:
            log.message.error_conn(mongo_connection.get_db_properties(), 'source')
        if not postgres_status:
            log.message.error_conn(postgres_connection.get_db_properties(), 'destination')
        return False


def initialize_destination():
    # get env variables
    DEST_HOSTNAME = os.getenv('DEST_HOSTNAME')
    DEST_PORT = os.getenv('DEST_PORT')
    DEST_DB = os.getenv('DEST_DB')
    DEST_ID = os.getenv('DEST_ID')
    DEST_PASSWORD = os.getenv('DEST_PASSWORD')
    DEST_SCHEMA = 'etl'
    db_properties_destination = DbProperties(DEST_HOSTNAME, DEST_PORT,
                                             DEST_DB, DEST_ID,
                                             DEST_PASSWORD, DEST_SCHEMA)
    return db_properties_destination


def initialize_source():
    SRC_HOSTNAME = os.getenv('SRC_HOSTNAME')
    SRC_PORT = os.getenv("SRC_PORT")
    SRC_DB = os.getenv('SRC_DB')
    SRC_ID = os.getenv('SRC_ID')
    SRC_PASSWORD = os.getenv('SRC_PASSWORD')
    SRC_SCHEMA = os.getenv('SRC_SCHEMA')

    db_properties_source = DbProperties(SRC_HOSTNAME, SRC_PORT,
                                        SRC_DB, SRC_ID,
                                        SRC_PASSWORD, SRC_SCHEMA)
    return db_properties_source


if __name__ == '__main__':
    try:
        run()
    except RuntimeError as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.message.log_stack_trace(err, file_name, exc_tb.tb_lineno)
