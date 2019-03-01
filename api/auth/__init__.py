from api.auth.model import User, find_user
from api.mongo import db
from werkzeug.security import safe_str_cmp
from bson import ObjectId
from validate_email import validate_email
from flask import Blueprint, request
from flask_jwt import current_identity, jwt_required

create_user_blueprint = Blueprint('create_user', __name__)


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
import json



def validate_user(user):
    is_valid = True
    errors = ""
    if db.users.find({"username": user.username}).count() > 0:
        errors = "username already exists"
        is_valid = False
    if not validate_email(user.username):
        errors += "email not valid \n"
        is_valid = False
    if user.role != "admin" and user.role != "user":
        print(user.role)
        errors += "user role not valid (user or admin) \n"
        is_valid = False
    if not isinstance(user.devices, list):
        errors += "devices must be a list \n"
        is_valid = False
    else:
        for value in user.devices:
            if not isinstance(value, str):
                errors += "device ids must be strings \n"
                is_valid = False

    return is_valid, errors

import pdb

@create_user_blueprint.route('/user', methods=['POST'])
@jwt_required()
def new_user():
    is_admin = current_identity["role"] == "admin"
    if is_admin:
        user = User(json.loads(request.data))
        is_valid, errors = validate_user(user)
        if is_valid:
            try:
                db.users.insert(user.__dict__)
                return "User created"
            except:
                return "User creation failed"
        else:
            return errors
    else:
        return "Contact the administrator"
