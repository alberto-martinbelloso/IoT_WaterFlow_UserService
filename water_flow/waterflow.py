from flask import Blueprint

from water_flow.influx import get_measurements

waterflow_blueprint = Blueprint('waterflow', __name__)


@waterflow_blueprint.route('/waterflow/device_id=<dev_id>&from=<f>&to=<t>')
def water(dev_id=None, f=None, t=None):
    # http://127.0.0.1:5000/waterflow/device_id=0&from=1550000000000000000&to=1551112831000000000
    measures = get_measurements(dev_id, f, t)
    return measures
