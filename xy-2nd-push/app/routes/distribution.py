from flask import Blueprint

distribution_bp = Blueprint("distribution", __name__)

@distribution_bp.route("/distribution")
def distribution():
    return "Distribution Page"