import pymongo
import util as log
import sys, os


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
        mongo_client = pymongo.MongoClient(parameter_string, serverSelectionTimeoutMS=2000)
        return mongo_client

    def check_connection(self):
        mongo_client = self.client
        try:
            mongo_client.server_info()
            return True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.message.log_stack_trace(e, fname, exc_tb.tb_lineno)
            return False

    def get_client(self):
        return self.client

    def get_db_properties(self):
        return self.db_properties
