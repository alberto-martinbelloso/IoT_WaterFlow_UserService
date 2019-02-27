from flask import Blueprint, request
from bson.json_util import dumps

from api.bills.bills import get_bills

bills_blueprint = Blueprint('bills', __name__)


@bills_blueprint.route('/bills')
def water():
    username = request.args.get('username')
    _bills = get_bills(username)
    bills_list = []
    for bill in _bills.find():
        bills_list.append({"username": bill["username"], "date": bill["date"], "import": bill["import"]})

    return dumps({"bills": bills_list, "count": len(bills_list)})
