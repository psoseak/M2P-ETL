<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> add previous working file
=======
import argparse
>>>>>>> - create db_properties class to store database properties
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

<<<<<<< HEAD

    #establishing postgresql connection
<<<<<<< HEAD
    try: 
=======
    try:
>>>>>>> add previous working file
        postgre_connection = psycopg2.connect(database="postgres", user="postgres", password="VMware1!", host="localhost", port="5432")
=======
    # establishing postgresql connection
    try:
        postgre_connection = psycopg2.connect(database="postgres", user="postgres", password="VMware1!",
                                              host="localhost", port="5432")
>>>>>>> - clean up postgres.py

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
    # get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('--host')
    parser.add_argument('--port')
    parser.add_argument('--db')
    args = parser.parse_args()

    db_properties = DbProperties(args.user, args.password,
                                 args.host, args.port, args.db)
    load_data('postgres', db_properties)
