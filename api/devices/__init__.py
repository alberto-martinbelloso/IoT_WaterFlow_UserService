from flask import Blueprint, request
from api.devices.devices import *

devices = Blueprint('devices', __name__)


@devices.route('/devices', methods=['GET', 'POST'])
def platform_devices():
    if request.method == 'POST':
        return post_device(request.get_json())
    else:
        return get_device()
