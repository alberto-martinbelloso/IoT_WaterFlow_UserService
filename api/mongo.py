import pymongo
import os
from flask import Blueprint

mongo_blueprint = Blueprint('mongo_blueprint', __name__)


host = 'localhost'

try:
    if os.environ["DEPLOY"]:
        host = os.environ["MONGO_HOST"]
except Exception as e:
    print("Running on develop environment")

client = pymongo.MongoClient(f"{host}")
db = client["app"]


def get_device(device_id):
    try:
        col = db['devices']
        return col.find_one({"device_id":device_id},{"_id":False})
    except:
        return None


@mongo_blueprint.route('/mongo_status')
def mongo():
    return db.command("serverStatus")["connections"]