from flask import Blueprint
from api.waterflow.influx import get_measurements
from flask import request, abort
from datetime import datetime

import calendar
import time

waterflow_blueprint = Blueprint('waterflow', __name__)


@waterflow_blueprint.route('/waterflow/<device_id>')
def water(device_id=None):
    f = request.args.get('from')
    t = request.args.get('to')
    try:
        if f is None:
            return abort(400)
        else:
            f = datetime.utcfromtimestamp(int(f))
            if t is None:
                t = datetime.utcfromtimestamp(dt2ts(datetime.now()))
            else:
                t = datetime.utcfromtimestamp(int(t))

            measures = get_measurements(device_id, f, t)
            return measures
    except Exception as e:
        return abort(400)


def dt2ts(dt):
    """Converts a datetime object to UTC timestamp

    naive datetime will be considered UTC.

    """

    return calendar.timegm(dt.utctimetuple())
