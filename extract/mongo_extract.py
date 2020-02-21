class Extract:
    def __init__(self, client):
        self.client = client
        self.databases = client.database_names()
    
    def print_all_collections_in_database(self, database_name):
        database = self.client[database_name]
        for collection_name in database.collection_names():
            print(collection_name)
            collection = database[collection_name]
            self.print_single_collection(collection)
            
    def print_single_collection(self, collection):
        print("mongo db entries: ")
        for document in collection.find():
            print (document)
    