import pandas as pd


def convert_dictionary_to_data_frame(py_dict):
    data_frame = pd.DataFrame.from_dict(py_dict, orient='index')
    data_frame.transpose()
    return data_frame


def convert_list_dictionary_to_dataframe(data, key, collection_name):
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


def convert_dictionary_details_to_dataframe(data, key, collection_name):
    # initialize
    df_all = pd.DataFrame()
    pd_name = None
    # tries to loop and convert it to a dataframe
    for collection_fields_doc in data:
        for item_key, item_value in collection_fields_doc.items():
            # get the primary rowid
            if item_key == '_id':
                row_id = item_value

            # loop through the dictionary
            if item_key != '_id':
                if pd_name is None:
                    pd_name = 'link_{collection_name}_{key}'.format(
                        collection_name=collection_name,
                        key=key
                    )

                dict_all = {}
                dict_all.update({'_id_{parent}'.format(parent=collection_name): str(row_id)})
                for item_value_loop_key, item_value_loop_value in item_value.items():
                    if isinstance(item_value_loop_value, dict):
                        for item_value_loop_value_inside_key, item_value_loop_value_inside_value \
                                in item_value_loop_value.items():
                            # column name
                            curr_column = '{parent}{child}'.format(
                                parent=item_value_loop_key,
                                child=item_value_loop_value_inside_key.title()
                            )
                            dict_all.update({curr_column: str(item_value_loop_value_inside_value)})
                    else:
                        dict_all.update({item_value_loop_key: item_value_loop_value})

                # convert the dictionary to dataframe
                df_curr = pd.DataFrame([dict_all])
                if df_all.empty:
                    df_all = df_curr
                else:
                    df_all = pd.concat([df_all, df_curr], ignore_index=True)

    return pd_name, df_all
