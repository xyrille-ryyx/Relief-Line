from flask import Blueprint, render_template, session, redirect, url_for

tracking_bp = Blueprint("tracking", __name__)


@tracking_bp.before_request
def require_login():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))


@tracking_bp.route("/issuance")
def issuance():
    return render_template("issuance.html")


@tracking_bp.route("/validation")
def validation():
    return render_template("validation.html")


@tracking_bp.route("/donations")
def donations():
    return render_template("donations.html")