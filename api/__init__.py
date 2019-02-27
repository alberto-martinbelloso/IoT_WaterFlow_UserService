from bson import ObjectId
from flask import Flask
from werkzeug.security import safe_str_cmp
from api.model_user import User
from api.mongo import mongo_blueprint, db
from api.devices import devices_blueprint
from api.influx import influx_blueprint

from flask_jwt import JWT, jwt_required, current_identity
import os

# secret = 'super-secret'
# try:
#     if os.environ["DEPLOY"]:
#         secret = str(os.environ["SECRET"])
# except ValueError:
#     print('INFO | Development secret key')
#
#
# def find_user(u, username):
#     for user in u:
#         if user["username"].encode('utf-8') == username.encode('utf-8'):
#             return user
#
#
# def authenticate(username, password):
#     user = find_user(_users, username)
#     if user and safe_str_cmp(user["password"].encode('utf-8'), password.encode('utf-8')):
#         return User(user)
#
#
# def identity(payload):
#     user_id = payload['identity']
#     return _collection.find_one({'_id': ObjectId(user_id)})


# create and configure the app

app = Flask(__name__)
# app.config['SECRET_KEY'] = secret

app.register_blueprint(mongo_blueprint)
app.register_blueprint(devices_blueprint)
app.register_blueprint(influx_blueprint)

_collection = db["users"]
_users = _collection.find({})

# JWT
# jwt = JWT(app, authenticate, identity)

@app.route("/")
def hello():
    return "Hello World!"

#
# @app.route('/protected')
# @jwt_required()
# def protected():
#     return '%s' % current_identity
