from cloud_nine.extensions import db
from cloud_nine.models import User, Flights
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/flights")
def flights():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if request.method == "POST":
        takeoff = request.form["name"]
        landing = request.form["password"]

        flight = Flights(takeoff=takeoff, landing=landing, flyer=current_user.id)
        
        db.session.add(flight)
        db.session.commit()
    
    booked_flights = Flights.query.filter_by(flyer=current_user.id).all()
    context = {
        'booked_flights' : booked_flights
    }

    return render_template('flights.html', **context)

@main.route("/programs")
def programs():
    return render_template("programs.html")

@main.route("/work")
def work():
    return render_template("work.html")

@main.route("/credits")
def credits():
    return render_template("credits.html")

@main.route("/privacy")
def privacy():
    return render_template("privacy.html")

@main.route("/terms")
def terms():
    return render_template("terms.html")