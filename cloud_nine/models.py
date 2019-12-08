from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from .extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    miles_flown = db.Column(db.Integer)
    flyer_miles = db.Column(db.Integer)
    cash_spent = db.Column(db.Integer)

    flights_booked = db.relationship(
        'Flights', 
        backref='user', 
        lazy=True
    )

    @property
    def unhashed_password(self):
        raise AttributeError("Cannot view unhashed password!")

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

class Flights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    takeoff = db.Column(db.String(50))
    landing = db.Column(db.String(50))
    distance = db.Column(db.Integer)
    date = db.Column(db.String(50))
    flyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
