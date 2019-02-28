from flask import Flask
from api.mongo import mongo_blueprint, db
from api.devices import devices_blueprint
from api.auth import identity, find_user, authenticate
from flask_jwt import JWT, jwt_required, current_identity

# create and configure the app


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

app.register_blueprint(mongo_blueprint)
app.register_blueprint(devices_blueprint)

jwt = JWT(app, authenticate, identity)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity
