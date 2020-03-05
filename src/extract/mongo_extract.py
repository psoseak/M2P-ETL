from transform.mongo_postgres_transform import convert_list_dictionary_to_dataframe
from util.message import *


class Extract:
    def __init__(self, client):
        self.client = client
        self.database_names = client.database_names()

    def extract_data_from_database(self, database_name):
        extracted_data = {}

        database = self.client[database_name]
        if not database.collection_names():
            info_extraction_database_empty(database_name)

        for collection_name in database.collection_names():
            field_key_list = []
            collection = database[collection_name]

            if collection.count() == 0:
                info_extraction_collection_empty(collection_name)

            document_first = collection.find_one()
            if document_first is not None:
                for key in document_first.keys():
                    if isinstance(document_first[key], list):
                        field_key_list.append(key)

                        # current dictionary
                        collection_fields = collection.find({}, {'_id': 1, key: 1})
                        df_new = convert_list_dictionary_to_dataframe(
                            collection_fields, key, collection_name)
                        # df_new = self.create_new_schema(collection_fields, key, collection_name)
                        extracted_data['link_' + collection_name + '_' + key] = df_new

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
