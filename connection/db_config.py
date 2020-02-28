class DbProperties:
    hostname = ''
    port = ''
    db = ''
    user = ''
    password = ''
    schema = ''

    # default constructor
    def __init__(self, hostname, port, db, user, password, schema):
        self.hostname = hostname
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.schema = schema
