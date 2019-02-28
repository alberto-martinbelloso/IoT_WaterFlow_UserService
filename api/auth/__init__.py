import json

from validate_email import validate_email
from flask import Blueprint, request
from flask_jwt import current_identity, jwt_required

from api.mongo import db
from api.auth.User import User

create_user_blueprint = Blueprint('create_user', __name__)


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


@create_user_blueprint.route('/user', methods=['POST'])
@jwt_required()
def new_user():
    is_admin = current_identity["role"].encode('utf-8') == "admin"
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
