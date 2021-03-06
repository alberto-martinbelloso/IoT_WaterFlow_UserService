from flask import jsonify
from api.mongo import db
from flask_jwt import current_identity
import datetime

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


def get_devices():
    devices = find_devices(current_identity['devices'], current_identity['role'])
    return jsonify({
        'devices': devices,
        'count': len(devices)
    }), 200


def find_devices(devices, role):
    if role == 'admin':
        return list(col.find({}, {'_id': False}))
    else:
        return list(col.find({'device_id': {'$in': devices}}, {'_id': False}))


def get_single_device(device_id):
    try:
        return col.find_one({"device_id": device_id}, {"_id": False})
    except:
        return None
