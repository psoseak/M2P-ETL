import pymongo


class MongoConnection:

    def __init__(self, db_properties):
        self.db_properties = db_properties
        self.client = self.initiate_connection()

    def initiate_connection(self):
        parameter_string = "mongodb://{user}:{password}@{hostname}:{port}/".format(
            user=self.db_properties.user,
            password=self.db_properties.password,
            hostname=self.db_properties.hostname,
            port=self.db_properties.port
        )
        print(parameter_string)
        mongo_client = pymongo.MongoClient(parameter_string)
        return mongo_client

    def get_client(self):
        return self.client
