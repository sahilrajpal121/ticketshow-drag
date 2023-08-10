from flask_restful import Resource, reqparse, marshal_with, fields
from application.db import db, Show, Venue
from application.access import acs_show_id
from .validation import PropertyExistError, BusinessValidationError, SchemaValidationError, NotFoundError
from flask_jwt_extended import jwt_required
from datetime import datetime
from application.helpers import admin_required, eval_get_list
from werkzeug.datastructures import FileStorage
from flask import request
import os


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name of the show', location='form')
parser.add_argument('tags', type=str, help='Tags of the show', location='form')
parser.add_argument('description', type=str, help='Description of the show', location='form')
parser.add_argument('rating', type=float, help='Rating of the show', location='form')
parser.add_argument('duration', type=int, help='Duration of the show', location='form')
parser.add_argument('price', type=str, help='Price of the show', location='form')
# add an image parser that takes file in binary format
parser.add_argument('image', type=FileStorage, help='Image of the show', location='files')
parser.add_argument('start_time', type=str, help='Start date of the show', location='form')
parser.add_argument('end_time', type=str, help='End date of the show', location='form')
# parser.add_argument('venues', type=str, help='Venues of the show', location='form', action='append')

response_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'tags': fields.String,
    'rating': fields.Float,
    'description': fields.String,
    'duration': fields.Integer,
    'price': fields.String,
    'image': fields.String,
    'start_time': fields.String,
    'end_time': fields.String,
    'venue_id': fields.Integer

}

class ShowAPI(Resource):
    @admin_required()
    @marshal_with(response_fields)
    def post(self):
        print('post')
        args = parser.parse_args()
        print('args')
        name = args['name']
        rating = args['rating']
        tags = args['tags']
        duration = args['duration']
        price = args['price']
        image = args['image']
        description = args['description']
        start_time = args['start_time']
        end_time = args['end_time']
        # venues = args['venues']

        
        data = request.form
        venues = data.get('venues')
        print('before', venues, type(venues))
        venues = eval_get_list(venues)
        print(type(venues))
        print(venues)

        
        if name is None:
            raise SchemaValidationError(400, 1001, 'Name is required')
        
        if tags is None:
            raise SchemaValidationError(400, 1002, 'Tags is required')
        
        if duration is None:
            raise SchemaValidationError(400, 1003, 'Duration is required')
        
        if price is None:
            raise SchemaValidationError(400, 1004, 'Price is required')
        
        if start_time is None:
            raise SchemaValidationError(400, 1005, 'Start date is required')
        
        if end_time is None:
            raise SchemaValidationError(400, 1006, 'End date is required')
        
        if rating is None:
            raise SchemaValidationError(400, 1007, 'Rating is required')
        
        if not venues:
            raise SchemaValidationError(400, 1008, 'Venues is required')
        
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
   
        if image:
            image_ext = image.mimetype.split('/')[-1]
            image_name = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.{image_ext}"
            image.save(os.path.join('../frontend/src/assets/images/shows', image_name))
        else:
            image_name = None
        
        # check if the show already exists with all the same values
        show = Show.query.filter_by(name=name, rating=rating, tags=tags, duration=duration, price=price, image=image_name, description=description, start_time=start_time, end_time=end_time).first()
        if show is not None:
            raise PropertyExistError(409, 'Show already exists')

        # add the show to the venues
        for venue_id in venues:
            print("venue", venue_id)
            show = Show(name=name, rating=rating, tags=tags, duration=duration, price=price, image=image_name, description=description, start_time=start_time, end_time=end_time, venue_id=venue_id)
            db.session.add(show)      
        db.session.commit()
        return show, 201
    
    # @jwt_required()
    @marshal_with(response_fields)
    def get(self, id=None):
        if id is None:
            shows = Show.query.all()
            return shows, 200
        else:
            show = acs_show_id(id=id)
            if show is None:
                raise NotFoundError(404)
            return show, 200
    
    @admin_required()
    @marshal_with(response_fields)
    def put(self, id):
        args = parser.parse_args()
        name = args['name']
        tags = args['tags']
        duration = args['duration']
        price = args['price']
        image = args['image']
        start_time = args['start_time']
        end_time = args['end_time']
        show = Show.query.filter_by(id=id).first()
        if show is None:
            raise NotFoundError(404, 'Show not found')
        if name and Show.query.filter_by(name=name).first():
                raise PropertyExistError(409, 'Show already exists')
        if name is not None:
            show.name = name
        if tags is not None:
            show.tags = tags
        if duration is not None:
            show.duration = duration
        if price is not None:
            show.price = price
        if image is not None:
            show.image = image
        if start_time is not None:
            show.start_time = start_time
        if end_time is not None:
            show.end_time = end_time

        db.session.commit()
        return show, 200
    
    @admin_required()
    @marshal_with(response_fields)
    def delete(self, id):
        show = Show.query.filter_by(id=id).first()
        if show is None:
            raise NotFoundError(404, 'Show not found')
        db.session.delete(show)
        db.session.commit()
        return show, 200
    