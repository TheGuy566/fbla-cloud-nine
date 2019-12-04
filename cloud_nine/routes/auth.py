from cloud_nine.extensions import db
from cloud_nine.models import User, Flights
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        unhashed_password = request.form["password"]

        user = User(name=name, unhashed_password=unhashed_password)
        
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("signup.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        user = User.query.filter_by(name=name).first()
        error_msg = ""

        if not user or not check_password_hash(user.password, password):
            error_msg = "Could not login. Please check and try again"
        if not error_msg:
            login_user(user)
            return redirect(url_for("main.index"))
        
    return render_template("login.html")

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@auth.route("/profile")
def profile():
    return render_template("profile.html")