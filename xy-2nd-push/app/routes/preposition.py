from flask import Blueprint, render_template, session, redirect, url_for

preposition_bp = Blueprint("preposition", __name__)


@preposition_bp.route("/preposition")
def preposition():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("preposition.html")
