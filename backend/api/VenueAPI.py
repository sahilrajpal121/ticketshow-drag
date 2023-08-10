from flask_restful import Resource, reqparse, marshal_with, fields
from application.db import db, Venue
from .validation import PropertyExistError, BusinessValidationError, SchemaValidationError, NotFoundError
from application.helpers import admin_required
from flask_jwt_extended import jwt_required
from flask import request

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name of the venue')
parser.add_argument('location', type=str, help='Location of the venue')
parser.add_argument('capacity', type=int, help='Capacity of the venue')
parser.add_argument('type', type=str, help='Type of the venue')
parser.add_argument('query', type=str, help='Query string for searching')

response_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'location': fields.String,
    'capacity': fields.Integer,
    'type': fields.String,
    'shows': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'tags': fields.String,
        'duration': fields.Integer,
        'price': fields.Integer,
        'description': fields.String,
        'image': fields.String,
        'rating': fields.Float,
        'start_time': fields.DateTime,
        'end_time': fields.DateTime,
        }))
}

class VenueAPI(Resource):
    @admin_required()
    @marshal_with(response_fields)
    def post(self):
        args = parser.parse_args()
        name = args['name']
        location = args['location']
        capacity = args['capacity']
        type = args['type']
        # for arg in args:
        #     print(arg, type(arg))
        if Venue.query.filter_by(name=name).first():
            raise PropertyExistError(409, 'Venue name already exists')
        
        if name is None:
            raise SchemaValidationError(400, 1001, 'Name is required')
        
        if location is None:
            raise SchemaValidationError(400, 1002, 'Location is required')
        
        if capacity is None:
            raise SchemaValidationError(400, 1003, 'Capacity is required')
        
        if type is None:
            raise SchemaValidationError(400, 1004, 'Type is required')
        
        venue = Venue(name=name, location=location, capacity=capacity, type=type)
        db.session.add(venue)
        db.session.commit()
        return venue, 201
    
    # @jwt_required()
    @marshal_with(response_fields)
    def get(self, id=None):
        # check if id is there, if not check if query is there. the query should check for name or location
        if id is not None:
            venue = Venue.query.filter_by(id=id).first()
            if venue is None:
                raise NotFoundError(404, 'Venue not found')
            return venue, 200
        else:
            query = request.args.get('search', '')
            print(query)
            if not query:
                venues = Venue.query.all()
                return venues, 200
            
            # check if query matches name or location with OR condition
            venues = Venue.query.filter(Venue.name.ilike('%'+query+'%') | Venue.location.ilike('%'+query+'%')).all()
            if venues is None:
                raise NotFoundError(404, 'Venue not found')
            return venues, 200
    
    @admin_required()
    @marshal_with(response_fields)
    def put(self, id):
        args = parser.parse_args()
        name = args['name']
        location = args['location']
        capacity = args['capacity']
        type = args['type']
        venue = Venue.query.filter_by(id=id).first()
        if venue is None:
            raise NotFoundError(404, 'Venue not found')
        if name is not None:
            venue.name = name
        if location is not None:
            venue.location = location
        if capacity is not None:
            venue.capacity = capacity
        if type is not None:
            venue.type = type
        db.session.commit()
        return venue, 200
    
    @admin_required()
    @marshal_with(response_fields)
    def delete(self, id):
        venue = Venue.query.filter_by(id=id).first()
        if venue is None:
            raise NotFoundError(404, 'Venue not found')
        db.session.delete(venue)
        db.session.commit()
        return venue, 200
    