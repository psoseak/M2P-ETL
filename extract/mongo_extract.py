class Extract:
    def __init__(self, client):
        self.client = client
        self.database_names = client.database_names()

    def print_all_databases(self):
        print(str(self.database_names))

    def print_all_collections_in_database(self, database_name):
        database = self.client[database_name]
        for collection_name in database.collection_names():
            print(collection_name)
            collection = database[collection_name]
            self.print_single_collection(collection)

    def print_single_collection(self, collection):
        for document in collection.find():
            print(document)

    def delete_database(self, database_name):
        self.client.drop_database(database_name)

    def create_database(self, database_name):
        return self.client[database_name]

    def extract_data_from_database(self, database_name):
        database = self.client[database_name]

        extracted_data = {}

        for collection_name in database.collection_names():
            if collection_name == "cards":
                collection = database[collection_name]
                # test
                sample = collection.find_one()
                # print(sample)
                print(sample.keys())
                print(type(sample['_id']))

                # self.create_new_schema()

                # continue
                extracted_collection = {}
                for document in collection.find():
                    extracted_collection[document["_id"]] = document
                    break

                extracted_data[collection_name] = extracted_collection

        return extracted_data

    def create_new_schema(self, data):
        print(data)
