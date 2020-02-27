import pandas as pd


class Transform:
    def __init__(self, data):
        self.data = data

    def print_all_data(self):
        print(self.data)

    def get_data(self):
        return self.data

    def convert_dictionary_to_data_frame(self, py_dict):
        df = pd.DataFrame.from_dict(py_dict, orient='index')
        df.transpose()
        return df
