from flask import Blueprint
import pymongo

mongo_blueprint = Blueprint('mongo', __name__)


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["app"]


@mongo_blueprint.route('/mongo_status')
def mongo():
    return "OK"
