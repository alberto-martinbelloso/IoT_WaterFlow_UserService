from flask import Flask
from api.auth import authenticate, identity
from api.mongo import mongo_blueprint
from api.devices import devices_blueprint
from flask_jwt import JWT, jwt_required, current_identity
import os

secret = 'super-secret'
try:
    if os.environ["DEPLOY"]:
        host = os.environ["SECRET"]
except:
    print('INFO | Development secret key')
# create and configure the app

app = Flask(__name__)
app.config['SECRET_KEY'] = secret

app.register_blueprint(mongo_blueprint)
app.register_blueprint(devices_blueprint)
app.register_blueprint(devices_blueprint)


# JWT
jwt = JWT(app, authenticate, identity)

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity
