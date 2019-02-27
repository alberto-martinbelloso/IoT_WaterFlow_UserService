from flask import Flask
from api.mongo import mongo_blueprint
# create and configure the app

app = Flask(__name__)
app.register_blueprint(mongo_blueprint)



@app.route("/")
def hello():
    return "Hello World!"