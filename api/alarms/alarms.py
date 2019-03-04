from api.mongo import db


def get_alarms_from_device(device_id):
    alarms = db['alarms'].find({
        'device_id': device_id
    }, {'_id': False})
    return list(alarms)


def get_all_alarms(f):
    if f is None:
        f = 0
    alarms = db['alarms'].find({}, {'_id': False}).skip(f).limit(20)
    return list(alarms)
