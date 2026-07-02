from flask import Blueprint

warehouse_bp = Blueprint("warehouse", __name__)

@warehouse_bp.route("/warehouse")
def warehouse():
    return "Warehouse Page"