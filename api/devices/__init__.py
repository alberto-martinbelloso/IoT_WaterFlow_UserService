from flask import Blueprint, request
from api.devices.devices import *
from flask_jwt import jwt_required

devices = Blueprint('devices', __name__)


@devices.route('/devices', methods=['GET', 'POST'])
@jwt_required()
def platform_devices():
    if request.method == 'POST':
        if current_identity['role'] != 'admin':
            return jsonify({'message': 'Invalid action'}), 401
        return post_device(request.get_json())
    else:
        return get_device()
