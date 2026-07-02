from flask import Blueprint, render_template, session, redirect, url_for

allocation_bp = Blueprint("allocation", __name__)


@allocation_bp.route("/allocation")
def allocation():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("allocation.html")