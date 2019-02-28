class User(object):
    def __init__(self, user):
        self.id = str(user["_id"])
        self.username = user["username"].encode('utf-8')
        self.password = user["password"].encode('utf-8')
        self.devices = [d.encode('utf-8') for d in user["devices"]]
        self.role = user["role"].encode('utf-8')

    def __str__(self):
        return "User(id='%s')" % self.id
