from flask_restful import Resource, reqparse, marshal_with, fields
from application.db import db, Booking, Show, User
from .validation import PropertyExistError, BusinessValidationError, SchemaValidationError, NotFoundError
from flask_jwt_extended import jwt_required
from datetime import datetime
from application.helpers import admin_required
from flask import request

parser = reqparse.RequestParser()
parser.add_argument('show_id', type=int, help='Show ID')
parser.add_argument('user_id', type=int, help='Venue ID')
parser.add_argument('num_seats', type=int, help='Number of seats')

response_fields = {
    'id': fields.Integer,
    'show_id': fields.Integer,
    'user_id': fields.Integer,
    'num_seats': fields.Integer,
    "show": fields.Nested({
        'name': fields.String,
        'image': fields.String,
        'start_time': fields.DateTime(dt_format='iso8601'),
        'venue': fields.Nested({
            'name': fields.String,
            'location': fields.String,
            }),
        }),
}


class BookingAPI(Resource):
    @jwt_required()
    @marshal_with(response_fields)
    def post(self):
        args = parser.parse_args()
        show_id = args['show_id']
        user_id = args['user_id']
        num_seats = args['num_seats']
        print(show_id, user_id, num_seats)

        show = Show.query.get(show_id)
        user = User.query.get(user_id)

        if show is None:
            raise NotFoundError('Show not found')
        if user is None:
            raise NotFoundError('Venue not found')
        
        booked_tickets = Booking.query.filter_by(show_id=show_id).all()
        num_booked_tickets = sum([booking.num_seats for booking in booked_tickets])

        if num_booked_tickets + num_seats > show.venue.capacity:
            raise BusinessValidationError(400, 'USER00', 'Not enough seats')

        booking = Booking(show_id=show_id, user_id=user_id, num_seats=num_seats)
        db.session.add(booking)
        db.session.commit()

        return booking, 200

    @jwt_required()
    @marshal_with(response_fields)
    def get(self):
        show_id = request.args.get('show_id')
        user_id = request.args.get('user_id')
        if show_id and user_id:
            bookings = Booking.query.filter_by(show_id=show_id, user_id=user_id).all()
        elif show_id:
            bookings = Booking.query.filter_by(show_id=show_id).all()
        elif user_id:
            bookings = Booking.query.filter_by(user_id=user_id).all()
        else:
            bookings = Booking.query.all()
        return bookings, 200

