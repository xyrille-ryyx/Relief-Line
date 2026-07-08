from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import role_required

pswdo_bp = Blueprint("pswdo", __name__)

@pswdo_bp.route("/dashboard")
@login_required
@role_required("pswdo_admin", "system_admin")
def dashboard():
    return render_template("pswdo/dashboard.html")