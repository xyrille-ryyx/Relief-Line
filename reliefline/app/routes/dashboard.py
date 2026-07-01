from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    if session["role"] == "pswdo_admin":
        return render_template("dashboard_pswdo.html")
    
    # Other roles will have their own dashboard later
    return f"Welcome {session['name']} — Role: {session['role']}"