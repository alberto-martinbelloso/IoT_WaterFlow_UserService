class User(object):
    def __init__(self, user):
        if "_id" in user:
            self.id = str(user["_id"])
        self.username = str(user["username"])
        self.password = str(user["password"])
        self.devices = [str(d) for d in user["devices"]]
        self.role = str(user["role"])

    def __str__(self):
        return "User(id='%s')" % self.id


def find_user(u, username):
    for user in u:
        if user["username"].encode('utf-8') == username.encode('utf-8'):
            return user
