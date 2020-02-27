from pprint import pprint
import pandas as pd


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
                field_key_list = []
                collection = database[collection_name]
                # test
                sample = collection.find_one()
                for key in sample.keys():
                    # print(key)
                    # print(type(sample[key]))
                    if type(sample[key]) is list:
                        field_key_list.append(key)
                        # print('list_' + collection_name + '_' + key)

                        # current dictionary
                        test = collection.find({}, {'_id': 1, key: 1})
                        self.create_new_schema(test, key, collection_name)

                # print(field_key_list)

                # continue
                extracted_collection = {}
                for document in collection.find():
                    # drop the specific column
                    extracted_collection[document["_id"]] = document
                    break

                extracted_data[collection_name] = extracted_collection

        return extracted_data

    def create_new_schema(self, data, key, collection_name):
        if key == 'customFields':
            df_all = None
            data_type = None
            for x in data:
                key_data = x[key]
                row_id = x['_id']
                row_size = len(key_data)
                list_key = [row_id] * row_size
                if row_size > 0:
                    # check if is array of string or dictionary
                    if isinstance(key_data[0], dict):
                        df_new = pd.DataFrame(x[key])
                        df_new['_id_{}'.format(collection_name)] = list_key
                        if df_all is None:
                            data_type = 'dict'
                            df_all = df_new
                        else:
                            df_all = pd.concat([df_all, df_new], ignore_index=True)

                    if isinstance(key_data[0], str):
                        df_new = pd.DataFrame(list(zip(list_key, key_data)))
                        if df_all is None:
                            data_type = 'str'
                            df_all = df_new
                        else:
                            # append to df_all and ignore index
                            df_all = pd.concat([df_all, df_new], ignore_index=True)

            if data_type == 'str':
                print(df_all.rename(columns={0: '_id_{}'.format(collection_name), 1: key}))
            else:
                print(df_all)

            return df_all
