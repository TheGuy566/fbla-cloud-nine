from cloud_nine.extensions import db
from cloud_nine.models import User, Flights
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        unhashed_password = request.form["password"]

        if len(name) == 0:
            flash("Please enter a username.", "warning")
            return render_template("signup.html")
        
        if len(unhashed_password) == 0:
            flash("Please enter a password.", "warning")
            return render_template("signup.html")

        if len(name) <= 6:
            flash("Username must be 7 characters or longer.", "warning")
            return render_template("signup.html")
        
        if len(unhashed_password) <= 4:
            flash("Password must be 5 characters or longer.", "warning")
            return render_template("signup.html")

        matched_users = User.query\
            .filter_by(name=name)\
            .all()
        
        if matched_users:
            flash("Username is already in use.", "danger")
            return render_template("signup.html")

        user = User(
            name=name,
            unhashed_password=unhashed_password,
            miles_flown=0,
            flyer_miles=0,
            cash_spent=0
        )
        
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("signup.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        if len(name) == 0:
            flash("Please enter a username.", "warning")
            return render_template("login.html")
        if len(password) == 0:
            flash("Please enter a password.", "warning")
            return render_template("login.html")

        user = User.query.filter_by(name=name).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid Username or Password.", "danger")
            return render_template("login.html")
        
        login_user(user)
        flash("Login Successful!", "success")
        return redirect(url_for("main.index"))
        
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout Successful!", "success")
    return redirect(url_for("main.index"))
