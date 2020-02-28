from transform.data_transform import Transform


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
        # initialize data transform
        data_transformer = Transform()
        database = self.client[database_name]

        extracted_data = {}

        for collection_name in database.collection_names():
            field_key_list = []
            collection = database[collection_name]
            document_first = collection.find_one()
            if document_first is not None:
                for key in document_first.keys():
                    if type(document_first[key]) is list:
                        field_key_list.append(key)

                        # current dictionary
                        collection_fields = collection.find({}, {'_id': 1, key: 1})
                        df_new = data_transformer.convert_list_dictionary_to_dataframe(collection_fields,
                                                                                       key, collection_name)
                        # df_new = self.create_new_schema(collection_fields, key, collection_name)
                        extracted_data['list_' + collection_name + '_' + key] = df_new

            # continue
            extracted_collection = {}
            for document in collection.find():
                # drop columns that are is list
                if field_key_list != 0:
                    for field in field_key_list:
                        del document[field]

                extracted_collection[document["_id"]] = document

            extracted_data[collection_name] = extracted_collection

        return extracted_data
