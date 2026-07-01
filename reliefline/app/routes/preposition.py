from flask import Blueprint

preposition_bp = Blueprint("preposition", __name__)

@preposition_bp.route("/preposition")
def preposition():
    return "Preposition Page"