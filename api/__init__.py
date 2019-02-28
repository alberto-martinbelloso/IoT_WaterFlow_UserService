from flask import Flask
from api.mongo import mongo_blueprint, db
from api.devices import devices_blueprint
from api.models import User, find_user
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

# create and configure the app


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


app = Flask(__name__)

app.register_blueprint(mongo_blueprint)
app.register_blueprint(devices_blueprint)

_collection = db["users"]
_users = _collection.find({})

jwt = JWT(app, authenticate, identity)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity
