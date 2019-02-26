from flask import jsonify
from api.mongo import db
from flask_jwt import current_identity
import datetime

vexpr = {"$jsonSchema":
    {
        "bsonType": "object",
        "required": ["device_id", "threshold"],
        "properties": {
            "device_id": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "threshold": {
                "bsonType": "number",
                "description": "must be a number and is required"
            },

            "created": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
        }
    }
}
keys = {'device_id', 'threshold'}

if 'devices' not in db.collection_names():
    db.create_collection('devices', validator={'validator': vexpr})

col = db['devices']


def post_device(data):
    now = datetime.datetime.now()
    data['created'] = str(now)
    col.insert(data)

    resp = jsonify({
        "device_id": data["device_id"],
        "threshold": data["threshold"],
        "created": data['created']
    })
    resp.status_code = 200
    return resp


def get_device():
    devices = find_devices(current_identity['devices'])
    return jsonify({
        'devices': devices,
        'count': len(devices)
    }), 200


def find_devices(devices):
    return list(col.find({"device_id": {"$in": devices}}, {'_id': False}))
