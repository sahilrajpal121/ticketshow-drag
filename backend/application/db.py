from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
import datetime
import pytz

Base = declarative_base()
db = SQLAlchemy()


IST = pytz.timezone('Asia/Kolkata')


UserRoles = db.Table('UserRoles',
                     db.Column('user_id', db.Integer(),
                               db.ForeignKey('User.id')),
                     db.Column('role_id', db.Integer(),
                               db.ForeignKey('Role.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), default=True)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=UserRoles,
                            backref=db.backref('users', lazy='dynamic'))



class Role(db.Model, RoleMixin):
    __tablename__ = 'Role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=False)
    tags = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    shows = db.relationship('Show', backref='venue')

class Booking(db.Model):
    __tableName__ = 'Booking'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('Show.id'))
    num_seats = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    # seats = db.Column(db.String(255), nullable=False)
    user = db.relationship('User', backref='bookings')
    show = db.relationship('Show', backref='bookings')

    def __init__(self, user_id, show_id, num_seats, time=None):
        self.user_id = user_id
        self.show_id = show_id
        self.num_seats = num_seats
        if time:
            self.time = time
        else:
            self.time = datetime.datetime.now(IST)
# class Screening(db.Model):
#     __tableName__ = 'Screening'
#     show_id = db.Column(db.Integer, db.ForeignKey('Show.id'))
#     venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
#     show = db.relationship('Show', backref='screenings')
#     venue = db.relationship('Venue', backref='screenings')




    