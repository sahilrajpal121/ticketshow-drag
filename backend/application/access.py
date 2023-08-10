from application.db import User, Booking, Show, Venue
from application.cache import cache

@cache.memoize()
def acs_user_email(email):
    return User.query.filter_by(email=email).first()

@cache.memoize()
def acs_user_id(id):
    return User.query.filter_by(id=id).first()

@cache.memoize()
def acs_user_all():
    return User.query.all()

@cache.memoize()
def acs_user_booking(id):
    return Booking.query.filter_by(user_id=id).first()

@cache.memoize()
def acs_venue_booking(id):
    return Booking.query.filter_by(venue_id=id).first()

@cache.memoize()
def acs_show_id(id):
    return Show.query.filter_by(id=id).first()



