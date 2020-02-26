import argparse
import os
import psycopg2
import pymongo
from load.postgres import test_retrieve_postgres
from load.postgres import upsert_table
from connection.db_config import DbProperties
from connection.mongo_connection import MongoConnection
from transform.data_transform import Transform
from extract.mongo_extract import Extract

def run_main_sequence(mongo_address, mongo_db, db_properties):
    mongo_connection = MongoConnection(mongo_address,27017) #default port 27017
    extraction_instance = Extract(mongo_connection.get_client())
    wekan_data = extraction_instance.extract_data_from_database(mongo_db)
    data_transformer = Transform(wekan_data)


    for collection in wekan_data:
        collection_data_frame = data_transformer.convert_dictionary_to_data_frame(wekan_data[collection]) #testing to convert this object to df
        #upsert_table(collection_data_frame, 'wekan', collection, db_properties)


def load_data(db, db_properties):
    if db == 'postgres':
        test_retrieve_postgres(db_properties)


def test_weihan():
    # get env variables
    DEST_HOSTNAME = os.getenv('DEST_HOSTNAME')
    DEST_PORT = os.getenv('DEST_PORT')
    DEST_DB = os.getenv('DEST_DB')
    DEST_ID = os.getenv('DEST_ID')
    DEST_PASSWORD = os.getenv('DEST_PASSWORD')
    db_properties_postgres = DbProperties(DEST_HOSTNAME, DEST_PORT, DEST_DB, DEST_ID, DEST_PASSWORD)
    load_data('postgres', db_properties_postgres)
    return db_properties_postgres

def test_justus(db_properties):

    SRC_HOSTNAME=os.getenv('SRC_HOSTNAME')
    SRC_DB=os.getenv('SRC_DB')
    SRC_ID=os.getenv('SRC_ID')
    SRC_PASSWORD=os.getenv('SRC_PASSWORD')
    run_main_sequence(SRC_HOSTNAME, SRC_DB, db_properties) #relative

if __name__ == '__main__':
    db_properties = test_weihan()
    test_justus(db_properties)
