from flask import Blueprint, render_template, session, redirect, url_for

provincial_bp = Blueprint("provincial", __name__)

@provincial_bp.route("/provincial")
@provincial_bp.route("/provincial-overview")
def provincial_overview():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("provincial_overview.html")