import pymongo

class MongoConnection:

    def __init__(self, mongodb_ip_address, port_num):
        self.mongodb_ip_address = mongodb_ip_address
        self.port_num = port_num
        self.client = self.initiate_connection()

    def initiate_connection(self):
        parameter_string = "mongodb://"+str(self.mongodb_ip_address)+":"+str(self.port_num)+"/"
        mongo_client = pymongo.MongoClient(parameter_string)
        return mongo_client       

    def get_client(self):
        return self.client