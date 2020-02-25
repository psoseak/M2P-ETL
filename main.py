import argparse
import psycopg2
import pymongo
from load.postgres import test_retrieve_postgres
from load.postgres import upsert_table
from connection.db_config import DbProperties
from connection.mongo_connection import MongoConnection
from transform.data_transform import Transform
from extract.mongo_extract import Extract #has to be relative in the future



def load_data(db, db_properties):
    if db == 'postgres':
        test_retrieve_postgres(db_properties)

def run_main_sequence(mongo_address, mongo_db, db_properties):
    mongo_connection = MongoConnection(mongo_address,27017) #default port 27017
    extraction_instance = Extract(mongo_connection.get_client())
    wekan_data = extraction_instance.extract_data_from_database(mongo_db)
    data_transformer = Transform(wekan_data)


    for collection in wekan_data:
        collection_data_frame = data_transformer.convert_dictionary_to_data_frame(wekan_data[collection]) #testing to convert this object to df
        #upsert_table(collection_data_frame, 'wekan', collection, db_properties)
        

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

    run_main_sequence(args.mongoaddress, args.mongodb, db_properties)
