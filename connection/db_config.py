class DbProperties:
    user = ''
    password = ''
    host = ''
    port = ''
    db = ''

    # default constructor
    def __init__(self, user, password, host, port, db):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db
