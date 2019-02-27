from flask import jsonify
from api.mongo import db
import datetime

if 'devices' not in db.collection_names():
    db.create_collection('devices')

col = db['devices']


def post_device(data):
    data['created'] = str(datetime.datetime.now())
    col.insert(data)

    resp = jsonify({
        "device_id": data["device_id"],
        "threshold": data["threshold"],
        "created": data['created']
    })
    resp.status_code = 200
    return resp


def get_device():
    devices = find_devices(["2"],'admin')
    return jsonify({
        'devices': devices,
        'count': len(devices)
    }), 200


def find_devices(devices, role):
    if role == 'admin':
        return list(col.find({}, {'_id': False}))
    else:
        return list(col.find({'device_id': {'$in': devices}}, {'_id': False}))
