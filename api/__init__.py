from flask import Flask
from api.mongo import mongo_blueprint, db
from api.devices import devices_blueprint
from api.auth import identity, find_user, authenticate
from api.waterflow import waterflow_blueprint
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
from api.auth import create_user_blueprint
from api.alarms import alarms_module
from api.auth.model import User
from api.bills import bills_blueprint
from api.mongo import mongo_blueprint, db
from api.devices import devices
from api.bills.generate_bills import job


import os
# create and configure the app

secret = 'super-secret'

try:
    if os.environ["DEPLOY"]:
        secret = os.environ["SECRET"]
except Exception as e:
    print("Running on develop environment")


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = secret

app.register_blueprint(mongo_blueprint)
app.register_blueprint(devices_blueprint)
app.register_blueprint(waterflow_blueprint)
app.register_blueprint(bills_blueprint)
app.register_blueprint(create_user_blueprint)
app.register_blueprint(alarms_module)

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
