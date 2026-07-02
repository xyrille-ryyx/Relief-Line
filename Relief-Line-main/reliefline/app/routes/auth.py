from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app import mysql

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def landing():
    return render_template("landing.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email")
        password = request.form.get("password")

        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id, name, email, password, role, office_id FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):
            session["user_id"]   = user[0]
            session["name"]      = user[1]
            session["email"]     = user[2]
            session["role"]      = user[4]
            session["office_id"] = user[5]
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid email or password.")
            return redirect(url_for("auth.login"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.landing"))