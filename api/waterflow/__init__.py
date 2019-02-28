from flask import Blueprint
from api.waterflow.influx import get_measurements

waterflow_blueprint = Blueprint('waterflow', __name__)


@waterflow_blueprint.route('/waterflow/device_id=<dev_id>&from=<f>&to=<t>')
def water(dev_id=None, f=None, t=None):
    measures = get_measurements(dev_id, f, t)
    return measures
