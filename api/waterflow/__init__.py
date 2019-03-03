from flask import Blueprint
from api.waterflow.waterflow import get_measurements
from flask import request, abort, jsonify
from flask_jwt import jwt_required, current_identity

import calendar

waterflow_blueprint = Blueprint('waterflow', __name__)


@waterflow_blueprint.route('/waterflow/<device_id>')
@jwt_required()
def water(device_id=None):
    f = request.args.get('from')
    t = request.args.get('to')
    group = request.args.get('group')
    try:
        if f is None or t is None:
            return abort(400)
        else:
            t = int(t) * 1000000
            f = int(f) * 1000000
            measures = []
            if current_identity['role'] == 'admin':
                print('admin')
                measures = get_measurements(device_id, int(f), int(t), group)
            else:
                if device_id not in current_identity['devices']:
                    return abort(404)
                else:
                    measures = get_measurements(device_id, int(f), int(t), group)
            return jsonify(measures), 200

    except Exception as e:
        print(e)
        return abort(400)


def dt2ts(dt):
    """Converts a datetime object to UTC timestamp

    naive datetime will be considered UTC.

    """

    return calendar.timegm(dt.utctimetuple())
