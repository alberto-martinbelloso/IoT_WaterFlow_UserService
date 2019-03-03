from flask import Blueprint, jsonify, request
from flask_jwt import current_identity, jwt_required
from api.alarms.alarms import get_alarms_from_device, get_all_alarms

alarms_module = Blueprint('alarms_module', __name__)


@alarms_module.route('/alarms', methods=['GET'])
@jwt_required()
def get_alarms():
    if current_identity['role'] == 'admin':
        f = request.args.get('from')
        return jsonify(get_all_alarms(f))
    else:
        alarms = {}
        for device_id in current_identity['devices']:
            alarms[device_id] = get_alarms_from_device(device_id)
        return jsonify(alarms), 200
