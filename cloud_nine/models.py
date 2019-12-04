from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from .extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))

    flights_booked = db.relationship(
        'Flights', 
        foreign_keys='Flights.flyer', 
        #backref='flyer', 
        lazy=True
    )

    @property
    def unhashed_password(self):
        raise AttributeError("Cannot view unhashed password!")

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

class Flights(db.Model):
    cities = ['Atlanta', 'Austin', 'Baton_Rogue', 'Columbia', 'D.C.', 'Jackson', 'Las Vegas',
    'Little_Rock','Long_Beach', 'Miami', 'Montgomery', 'Nashville', 'New York', 'Olympia',
    'Orlando', 'Raligh', 'Sacremento', 'Salem', 'Sanfrancico', 'Tallahasse']
    positions = {'Atlanta':[33.7490, 84.3880], 'Austin':[30.2672, 97.7431], 'Baton_Rogue':[30.4515, 91.1871], 'Columbia':[34.0007, 81.0348],
    'D.C.':[38.9072, 77.0369], 'Jackson':[32.2988, 90.1848], 'Las Vegas':[36.1699, 115.1398], 'Little_Rock':[34.7465, 92.2896],
    'Long_Beach':[33.7701, 118.1937], 'Miami':[25.7617, 80.1918], 'Montgomery':[32.3792, 86.3077], 'Nashville':[36.1627, 86.7816],
    'New York':[40.7128, 74.0060], 'Olympia':[47.0379, 122.9007], 'Orlando':[28.5383, 81.3792], 'Raligh':[35.7796, 78.6382],
    'Sacremento':[38.5816, 121.4944], 'Salem':[44.9429, 123.0351], 'Sanfrancico':[38.5816, 121.4944], 'Tallahasse':[30.4383, 84.2807]}
    id = db.Column(db.Integer, primary_key=True)
    takeoff = db.Column(db.Text)
    landing = db.Column(db.Text)
    flyer = db.Column(db.ForeignKey('user.id'))