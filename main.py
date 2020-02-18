<<<<<<< HEAD

=======
>>>>>>> add previous working file
import psycopg2
import pymongo


def main():

    #establishing mongo connection
    try:
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        mongo_db = mongo_client["mydatabase"] # creating database
        mongo_col = mongo_db["customers"] # creating collection

    except (Exception) as error:
        print(error)
        print("failed to connect to mongo db")

    else: 
        print("successfully connected to mongo")
        print_mongo_db(mongo_client, mongo_db, mongo_col)


    #establishing postgresql connection
<<<<<<< HEAD
    try: 
=======
    try:
>>>>>>> add previous working file
        postgre_connection = psycopg2.connect(database="postgres", user="postgres", password="VMware1!", host="localhost", port="5432")

    except (Exception, psycopg2.Error) as error:
        print("failed to connect to postgresql")
    
    else: 
        print("successfully connected to postgresql")


def print_mongo_db(mongo_client, mongo_db, mongo_col):
    print("mongo db entries: ")
    for document in mongo_col.find():
        print (document)

if __name__ == '__main__':
   main()

