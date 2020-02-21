import argparse
import os
import psycopg2
import pymongo
from load.postgres import test_retrieve_postgres
from connection.db_config import DbProperties


def main():
    # establishing mongo connection
    try:
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        mongo_db = mongo_client["mydatabase"]  # creating database
        mongo_col = mongo_db["customers"]  # creating collection

    except (Exception) as error:
        print(error)
        print("failed to connect to mongo db")

    else:
        print("successfully connected to mongo")
        print_mongo_db(mongo_client, mongo_db, mongo_col)

    # establishing postgresql connection
    try:
        postgre_connection = psycopg2.connect(database="postgres", user="postgres", password="VMware1!",
                                              host="localhost", port="5432")

    except (Exception, psycopg2.Error) as error:
        print("failed to connect to postgresql")

    else:
        print("successfully connected to postgresql")


def print_mongo_db(mongo_client, mongo_db, mongo_col):
    print("mongo db entries: ")
    for document in mongo_col.find():
        print(document)


def load_data(db, db_properties):
    if db == 'postgres':
        test_retrieve_postgres(db_properties)


if __name__ == '__main__':
    # # get arguments
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--user')
    # parser.add_argument('--password')
    # parser.add_argument('--host')
    # parser.add_argument('--port')
    # parser.add_argument('--db')
    # args = parser.parse_args()
    #
    # db_properties = DbProperties(args.user, args.password,
    #                              args.host, args.port, args.db)
    # load_data('postgres', db_properties)

    print('run1')
    # get env variables
    DEST_HOSTNAME = os.getenv('DEST_HOSTNAME')
    print(DEST_HOSTNAME)
    DEST_PORT = os.getenv('DEST_PORT')
    print(DEST_PORT)
    DEST_DB = os.getenv('DEST_DB')
    print(DEST_DB)
    DEST_ID = os.getenv('DEST_ID')
    print(DEST_ID)
    DEST_PASSWORD = os.getenv('DEST_PASSWORD')
    print(DEST_PASSWORD)
    db_properties_postgres = DbProperties(DEST_HOSTNAME, DEST_PORT, DEST_DB, DEST_ID, DEST_PASSWORD)
    load_data('postgres', db_properties_postgres)
