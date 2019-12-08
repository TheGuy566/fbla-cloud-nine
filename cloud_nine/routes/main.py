from cloud_nine.extensions import db
from cloud_nine.models import User, Flights
from flask import Blueprint, render_template, request, redirect, url_for, session, escape, flash
from flask_login import current_user, login_required
from math import sin, cos, sqrt, atan2, radians
import datetime

cities = ['Atlanta', 'Austin', 'Baton Rogue', 'Columbia', 'D.C.', 'Jackson', 'Las Vegas',
'Little Rock','Long Beach', 'Miami', 'Montgomery', 'Nashville', 'New York', 'Olympia',
'Orlando', 'Raligh', 'Sacremento', 'Salem', 'Sanfrancico', 'Tallahasse']

positions = {'Atlanta':[33.7490, 84.3880], 'Austin':[30.2672, 97.7431], 'Baton Rogue':[30.4515, 91.1871], 'Columbia':[34.0007, 81.0348],
'D.C.':[38.9072, 77.0369], 'Jackson':[32.2988, 90.1848], 'Las Vegas':[36.1699, 115.1398], 'Little Rock':[34.7465, 92.2896],
'Long Beach':[33.7701, 118.1937], 'Miami':[25.7617, 80.1918], 'Montgomery':[32.3792, 86.3077], 'Nashville':[36.1627, 86.7816],
'New York':[40.7128, 74.0060], 'Olympia':[47.0379, 122.9007], 'Orlando':[28.5383, 81.3792], 'Raligh':[35.7796, 78.6382],
'Sacremento':[38.5816, 121.4944], 'Salem':[44.9429, 123.0351], 'Sanfrancico':[38.5816, 121.4944], 'Tallahasse':[30.4383, 84.2807]}

brochures = {'Atlanta':"https://www.atlanta.net/explore/", 'Austin':"https://www.austintexas.org/plan-a-trip/",
'Baton Rogue':"https://www.visitbatonrouge.com/things-to-do/",'Columbia':"https://www.experiencecolumbiasc.com/things-to-do/",
'D.C.':"https://washington.org/things-do-washington-dc", 'Jackson':"https://www.visitjackson.com/must-see-and-do",
'Las Vegas':"https://www.travelandleisure.com/travel-guide/las-vegas-nevada/things-to-do",
'Little Rock':"https://www.travelandleisure.com/travel-guide/little-rock/things-to-do",
'Long Beach':"https://www.visitlongbeach.com/", 'Miami':"https://www.travelandleisure.com/travel-guide/miami/things-to-do",
'Montgomery':"https://www.lonelyplanet.com/usa/the-south/montgomery", 'Nashville':"https://www.travelandleisure.com/travel-guide/nashville-tennessee",
'New York':"https://www.nycgo.com/", 'Olympia':"https://www.experienceolympia.com/explore/",
'Orlando':"https://www.visitorlando.com/en/things-to-do", 'Raligh':"https://www.visitraleigh.com/things-to-do/",
'Sacremento':"https://www.visitsacramento.com/visit/vistors-guide/", 'Salem':"https://www.travelsalem.com/things-to-do",
'Sanfrancico':"https://www.travelandleisure.com/travel-guide/san-francisco/things-to-do", 'Tallahasse':"https://www.visitflorida.com/en-us/cities/tallahassee.html"}

def calculate_distance(location_a, location_b):
    R = 6373.0
    lat1 = radians(location_a[0])
    lon1 = radians(location_a[1])
    lat2 = radians(location_b[0])
    lon2 = radians(location_b[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = int(R * c)

    return distance

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/flights", methods=['GET', 'POST'])
@login_required
def flights():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if request.method == "POST":
        takeoff = request.form["start_location"]
        landing = request.form["end_location"]
        date = request.form["date"]

        flights = Flights(
            takeoff=takeoff, 
            landing=landing,
            distance=calculate_distance(positions[takeoff], positions[landing]),
            flyer_id=current_user.id,
            date=date 
        )

        if takeoff == landing:
            flash("Start location and end location should not be the same.", "warning")
            return redirect(url_for('main.flights'))
        
        if date == "":
            flash("Please specify a date for your flight.", "warning")
            return redirect(url_for('main.flights'))

        today = datetime.datetime.now()
        formatted = today.strftime("%Y-%m-%d").split("-")
        
        if int(date.split("-")[0]) < int(formatted[0]) or \
            int(date.split("-")[1]) < int(formatted[1]) or \
            int(date.split("-")[2]) < int(formatted[2]):
            flash("Please input a date that has not occurred.", "danger")
            return redirect(url_for('main.flights'))

        current_user.miles_flown += calculate_distance(positions[takeoff], positions[landing])
        current_user.flyer_miles += calculate_distance(positions[takeoff], positions[landing])/2
        current_user.cash_spent += round(50 + (calculate_distance(positions[takeoff], positions[landing])/1.609)*0.11, 2)
        
        db.session.add(flights)
        db.session.commit()

        flash("Flight booked!", "success")
        return redirect(url_for('main.flights'))

    flight_book = Flights.query\
        .filter_by(flyer_id=current_user.id)\
        .all()

    context = {
        'flight_book' : flight_book,
        'locations': cities
    }
    return render_template('flights.html', **context)

@main.route("/programs")
def programs():
    return render_template("programs.html")

@main.route("/work")
def work():
    return render_template("work.html")

@main.route("/flyers")
def flyers():
    return render_template("flyers.html")

@main.route("/credits")
def credits():
    return render_template("credits.html")

@main.route("/privacy")
def privacy():
    return render_template("privacy.html")

@main.route("/terms")
def terms():
    return render_template("terms.html")

@main.route("/profile_stats")
@login_required
def profile_stats():
    flight_book = Flights.query\
        .filter_by(flyer_id=current_user.id)\
        .all()

    context = {
        'name': current_user.name,
        'miles': current_user.miles_flown,
        'money': current_user.cash_spent,
        'flight_book' : flight_book,
        'flyer_mi': current_user.flyer_miles

    }

    return render_template("profile.html", **context)

@main.route("/profile_notify")
@login_required
def profile_notify():
    today = datetime.datetime.now()
    formatted = today.strftime("%Y-%m-%d")

    flight_book = Flights.query\
        .filter_by(flyer_id=current_user.id)\
        .filter_by(date=formatted)\
        .all()

    context = {
        'name': current_user.name,
        'flight_book' : flight_book,
        'travel': brochures
    }

    return render_template("profile_notify.html", **context)

@main.route("/profile_booked", methods=['GET', 'POST'])
@login_required
def profile_booked():
    if request.method == 'POST':
        delete_me = request.form["delete"]
        delete_selected = Flights.query.filter_by(id=delete_me).first()

        flash("Flight deleted!", "success")

        db.session.delete(delete_selected)
        db.session.commit()

        return redirect(url_for('main.profile_booked'))
    
    flight_book = Flights.query\
        .filter_by(flyer_id=current_user.id)\
        .all()
    
    context = {
        'name': current_user.name,
        'flight_book' : flight_book,
    }

    return render_template("profile_booked.html", **context)
