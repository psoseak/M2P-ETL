import pandas as pd


class Transform:

    def convert_dictionary_to_data_frame(self, py_dict):
        data_frame = pd.DataFrame.from_dict(py_dict, orient='index')
        data_frame.transpose()
        return data_frame

    def convert_list_dictionary_to_dataframe(self, data, key, collection_name):
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
            df_all = df_all.rename(columns={0: '_id_{}'.format(collection_name), 1: key})

        return df_all
