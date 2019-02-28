from flask import Blueprint
from api.waterflow.influx import get_measurements
from flask import request, abort, jsonify
from datetime import datetime

import calendar

waterflow_blueprint = Blueprint('waterflow', __name__)


@waterflow_blueprint.route('/waterflow/<device_id>')
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

            measures = get_measurements(device_id, int(f) * 1000000000, int(t) * 1000000000)
            return jsonify(measures)
    except Exception as e:
        return abort(400)


def dt2ts(dt):
    """Converts a datetime object to UTC timestamp

    naive datetime will be considered UTC.

    """

    return calendar.timegm(dt.utctimetuple())
