class DbProperties:
    hostname = ''
    port = ''
    db = ''
    user = ''
    password = ''

    # default constructor
    def __init__(self, hostname, port, db, user, password):
        self.hostname = hostname
        self.port = port
        self.db = db
        self.user = user
        self.password = password
