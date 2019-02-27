from bson import ObjectId
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from api.mongo import db
from api.model_user import User

_collection = db["users"]
_users = _collection.find({})


def find_user(u, username):
    for user in u:
        if user["username"].encode('utf-8') == username.encode('utf-8'):
            return user


def authenticate(username, password):
    user = find_user(_users, username)
    if user and safe_str_cmp(user["password"].encode('utf-8'), password.encode('utf-8')):
        return User(user)


def identity(payload):
    user_id = payload['identity']
    return _collection.find_one({'_id': ObjectId(user_id)})