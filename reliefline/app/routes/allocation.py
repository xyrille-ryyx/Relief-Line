from flask import Blueprint

allocation_bp = Blueprint("allocation", __name__)

@allocation_bp.route("/allocation")
def allocation():
    return "Allocation Page"