from flask import Blueprint
from api.waterflow.influx import get_measurements
from flask import request, abort, jsonify
from datetime import datetime
from flask_jwt import jwt_required, current_identity

import calendar

waterflow_blueprint = Blueprint('waterflow', __name__)


@waterflow_blueprint.route('/waterflow/<device_id>')
@jwt_required()
def water(device_id=None):
    f = request.args.get('from')
    t = request.args.get('to')
    try:
        if f is None:
            return abort(400)
        else:
            f = datetime.utcfromtimestamp(int(f)).timestamp()
            if t is None:
                t = datetime.utcfromtimestamp(dt2ts(datetime.now())).timestamp()
            else:
                t = datetime.utcfromtimestamp(int(t)).timestamp()

            if current_identity['role'] != 'admin':
                measures = get_measurements(device_id, int(f) * 1000000000, int(t) * 1000000000)
            else:
                if device_id not in current_identity['devices']:
                    return abort(404)
                else:
                    measures = get_measurements(device_id, int(f) * 1000000000, int(t) * 1000000000)
            return jsonify(measures)
    except Exception as e:
        return abort(400)


def dt2ts(dt):
    """Converts a datetime object to UTC timestamp

    naive datetime will be considered UTC.

    """

    return calendar.timegm(dt.utctimetuple())
