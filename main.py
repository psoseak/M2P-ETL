import argparse
import psycopg2
from load.postgres import test_retrieve_postgres
from connection.db_config import DbProperties
from connection.mongo_connection import MongoConnection
from transform.data_transform import Transform

import os

from extract.mongo_extract import Extract #has to be relative in the future

def load_data(db, db_properties):
    if db == 'postgres':
        test_retrieve_postgres(db_properties)

if __name__ == '__main__':
    # get arguments

    #postgresql arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('--host')
    parser.add_argument('--port')
    parser.add_argument('--db')

    #mongodb arguments
    parser.add_argument('--mongoaddress')
    parser.add_argument('--mongodb')

    args = parser.parse_args()

    db_properties = DbProperties(args.user, args.password,
                                 args.host, args.port, args.db)

    load_data('postgres', db_properties)

    mongo_connection = MongoConnection(args.mongoaddress,27017) #default port 27017
    extraction_instance = Extract(mongo_connection.get_client())
    wekan_data = extraction_instance.extract_data_from_database(args.mongodb)
    data_transformer = Transform(wekan_data)
    data_transformer.convert_dictionary_to_data_frame(wekan_data["boards"]["DPojncq9H63MGq5M2"]) #testing to convert this object to df