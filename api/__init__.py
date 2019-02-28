from bson import ObjectId
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

from api.auth.User import User
from api.bills import bills_blueprint
from api.mongo import mongo_blueprint, db
from api.waterflow.influx import influx_blueprint
from api.waterflow.waterflow import waterflow_blueprint
from api.bills.generate_bills import job


def find_user(u, username):
    for user in u:
        if user["username"].encode('utf-8') == username:
            return user


def authenticate(username, password):
    user = find_user(_users, username)
    if user and safe_str_cmp(user["password"].encode('utf-8'), password.encode('utf-8')):
        return User(user)


def identity(payload):
    user_id = payload['identity']
    return _collection.find_one({'_id': ObjectId(user_id)})


app = Flask(__name__)
app.config.from_pyfile('../config.py')
app.config['SECRET_KEY'] = 'super-secret'
app.register_blueprint(mongo_blueprint)
app.register_blueprint(waterflow_blueprint)
app.register_blueprint(influx_blueprint)
app.register_blueprint(bills_blueprint)

_collection = db["users"]
_users = _collection.find({})

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route('/')
def init():
    return 'User Service'


if __name__ == '__main__':
    app.run()
