from flask import Blueprint
import pymongo
import os

mongo_blueprint = Blueprint('mongo', __name__)

host = "mongodb://localhost:27017/"

try:
    if os.environ["DEPLOY"]:
        host = os.environ["MONGO_HOST"]
except Exception as e:
    print("Running on develop environment")

client = pymongo.MongoClient(f"{host}")
db = client["app"]


@mongo_blueprint.route('/mongo_status')
def mongo():
    return "OK"
