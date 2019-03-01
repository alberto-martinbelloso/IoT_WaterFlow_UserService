from flask import Blueprint, jsonify
from flask_jwt import current_identity, jwt_required
from api.bills.bills import get_bills, get_all_bills

bills_blueprint = Blueprint('bills', __name__)


@bills_blueprint.route('/bills')
@jwt_required()
def display_bills():
    logged_user = str(current_identity["username"])
    is_admin = str(current_identity["role"]) == "admin"

    if is_admin:
        _bills = get_all_bills()
    else:
        _bills = get_bills(logged_user)

    bills_list = []
    for bill in _bills:
        bills_list.append({"username": bill["username"], "date": bill["date"], "import": bill["price"]})

    return jsonify({"bills": bills_list, "count": len(bills_list)})
