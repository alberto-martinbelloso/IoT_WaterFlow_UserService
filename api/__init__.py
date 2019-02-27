from flask import Flask
from api.mongo import mongo_blueprint
from api.devices import devices
# create and configure the app

app = Flask(__name__)
app.register_blueprint(mongo_blueprint)
app.register_blueprint(devices)



@app.route("/")
def hello():
    return "Hello World!"