from flask import Blueprint
import pymongo

mongo_blueprint = Blueprint('mongo', __name__)

def db_collection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["app"]
    col = db["users"]
    return col


@mongo_blueprint.route('/mongo_status')
def mongo():
    return "OK"
