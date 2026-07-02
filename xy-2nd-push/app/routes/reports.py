from flask import Blueprint, render_template, session, redirect, url_for

reports_bp = Blueprint("reports", __name__)


@reports_bp.before_request
def require_login():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))


@reports_bp.route("/reports")
def reports():
    return render_template("reports.html")