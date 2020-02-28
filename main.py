import os

from connection.db_config import DbProperties
from connection.mongo_connection import MongoConnection
from extract.mongo_extract import Extract
from transform.data_transform import Transform
from load.postgres import upsert_table
import pandas as pd
import util as log


def run():
    log.message.info_start()
    db_properties_source = initialize_source()
    db_properties_destination = initialize_destination()

    mongo_connection = MongoConnection(db_properties_source)
    extraction_instance = Extract(mongo_connection.get_client())
    wekan_data = extraction_instance.extract_data_from_database(db_properties_source.db)
    # TODO: test destination database
    log.message.info_database_connected()

    data_transformer = Transform()

    for collection in wekan_data:
        if type(wekan_data[collection]) is pd.DataFrame:
            upsert_table(wekan_data[collection], 'wekan', collection, db_properties_destination)
        else:
            collection_data_frame = data_transformer.convert_dictionary_to_data_frame(wekan_data[collection]).applymap(
                str)
            if collection_data_frame.size > 0:
                collection_data_frame = collection_data_frame.set_index("_id")

            upsert_table(collection_data_frame, 'wekan', collection, db_properties_destination)

    log.message.info_migrated_completed()


def initialize_destination():
    # get env variables
    # TODO: add scheme for destination
    DEST_HOSTNAME = os.getenv('DEST_HOSTNAME')
    DEST_PORT = os.getenv('DEST_PORT')
    DEST_DB = os.getenv('DEST_DB')
    DEST_ID = os.getenv('DEST_ID')
    DEST_PASSWORD = os.getenv('DEST_PASSWORD')
    db_properties_destination = DbProperties(DEST_HOSTNAME, DEST_PORT, DEST_DB, DEST_ID, DEST_PASSWORD)
    return db_properties_destination


def initialize_source():
    SRC_HOSTNAME = os.getenv('SRC_HOSTNAME')
    SRC_PORT = os.getenv("SRC_PORT")
    SRC_DB = os.getenv('SRC_DB')
    SRC_ID = os.getenv('SRC_ID')
    SRC_PASSWORD = os.getenv('SRC_PASSWORD')
    db_properties_source = DbProperties(SRC_HOSTNAME, SRC_PORT, SRC_DB, SRC_ID, SRC_PASSWORD)
    return db_properties_source


if __name__ == '__main__':
    run()
