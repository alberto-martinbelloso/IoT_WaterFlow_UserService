from api.auth.model import User, find_user
from api.mongo import mongo_blueprint, db
from werkzeug.security import safe_str_cmp
from bson import ObjectId


def find_user(u, username):
    for user in u:
        if user["username"].encode('utf-8') == username.encode('utf-8'):
            return user


def authenticate(username, password):
    _collection = db["users"]
    _users = _collection.find({})

    user = find_user(_users, username)
    if user and safe_str_cmp(user["password"].encode('utf-8'), password.encode('utf-8')):
        return User(user)


def identity(payload):
    _collection = db["users"]
    _users = _collection.find({})

    user_id = payload['identity']
    return _collection.find_one({'_id': ObjectId(user_id)})
